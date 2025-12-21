import os
import uuid
import logging
import time
from pathlib import Path
from datetime import datetime

from app.services.artifacts import load_pickle, load_metadata
from app.services.preprocessing import criar_features_transacao

logger = logging.getLogger("fraud_sentinel.inference")

# --------------------------------------------------
# Base da aplicação 
# --------------------------------------------------
# inference.py -> services -> app -> fraud_sentinel
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_STAGE = os.getenv("MODEL_STAGE", "prod") # dev, prod
MODELS_DIR = BASE_DIR / "models" / MODEL_STAGE

# --------------------------------------------------
# Caminhos dos artefatos
# --------------------------------------------------
XGB_MODEL_PATH = MODELS_DIR / "xgboost" / "xgboost_fraud_model.pkl"
XGB_METADATA_PATH = MODELS_DIR / "xgboost" / "metadata.json"
RF_MODEL_PATH = MODELS_DIR / "random_forest" / "random_forest_fraud_model.pkl"
RF_METADATA_PATH = MODELS_DIR / "random_forest" / "metadata.json"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor" / "preprocessor.pkl"
PREPROCESSOR_METADATA_PATH = MODELS_DIR / "preprocessor" / "metadata.json"

# --------------------------------------------------
# Carregamento dos artefatos
# --------------------------------------------------
xgb_model = load_pickle(XGB_MODEL_PATH, critical=True)
rf_model = load_pickle(RF_MODEL_PATH, critical=True)
preprocessor = load_pickle(PREPROCESSOR_PATH, critical=True)

xgb_metadata = load_metadata(XGB_METADATA_PATH)
rf_metadata = load_metadata(RF_METADATA_PATH)
preprocessor_metadata = load_metadata(PREPROCESSOR_METADATA_PATH)


def decidir_risco(probabilidade: float):
    """
    Regra de decisão baseada na probabilidade de fraude.
    """
    if probabilidade >= 0.8:
        return "CRÍTICO", "BLOQUEAR TRANSAÇÃO"
    elif probabilidade >= 0.6:
        return "ALTO", "SOLICITAR MFA"
    elif probabilidade >= 0.4:
        return "MÉDIO", "MONITORAR"
    else:
        return "BAIXO", "APROVAR TRANSAÇÃO"


def predict_transaction(transaction_data: dict) -> dict:
    """
    Executa a inferência de fraude usando XGBoost + Random Forest (ensemble).
    """
    start_time = time.time()

    # =========================
    # Feature engineering
    # =========================
    features_df = criar_features_transacao(transaction_data)
    X = preprocessor.transform(features_df)

    # =========================
    # Inferência
    # =========================
    proba_xgb = xgb_model.predict_proba(X)[0][1]
    proba_rf = rf_model.predict_proba(X)[0][1]

    ensemble_proba = (proba_xgb + proba_rf) / 2
    risk_level, action = decidir_risco(ensemble_proba)

    processing_time_ms = (time.time() - start_time) * 1000

    # =========================
    # Resposta da requisição
    # =========================
    return {
        "transaction_id": transaction_data.get("trans_num", "unknown"),
        "timestamp": datetime.now().isoformat(),

        "models": {
            "xgboost": round(float(proba_xgb), 4),
            "random_forest": round(float(proba_rf), 4)
        },

        "ensemble": {
            "fraud_probability": round(float(ensemble_proba), 4),
            "confidence": round(
                ensemble_proba if ensemble_proba >= 0.5 else 1 - ensemble_proba, 4
            ),
            "is_fraud": ensemble_proba >= 0.5,
            "risk_level": risk_level,
            "recommended_action": action
        },

        "model": {
            "strategy": "ensemble_mean",
            "versions": {
                "xgboost": xgb_metadata.get("version", "unknown"),
                "random_forest": rf_metadata.get("version", "unknown")
            },
            "preprocessor_version": preprocessor_metadata.get("version", "unknown")
        },

        "processing": {
            "processing_time_ms": round(processing_time_ms, 2)
        },

        "insights": {
            "transaction_value": float(transaction_data.get("amt", 0)),
            "location_distance_km": round(float(
                features_df["distancia_km"].iloc[0]
            ), 2) if "distancia_km" in features_df.columns else None
        },

        "metadata": {
            "request_id": str(uuid.uuid4()),
            "status": "success"
        }
    }
