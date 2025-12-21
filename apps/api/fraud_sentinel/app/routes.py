from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from app.schemas import PredictRequest, PredictResponse
from app.services.inference import predict_transaction
from app.utils import convert_to_python_types

# --------------------------------------------------
# Configuração do router
# --------------------------------------------------
router = APIRouter()
logger = logging.getLogger("fraud_sentinel.routes")


# --------------------------------------------------
# Health check
# --------------------------------------------------
@router.get("/")
def health_check():
    """
    Endpoint simples para verificar se a API está online.
    """
    return {
        "status": "online",
        "service": "Fraud Sentinel API",
        "timestamp": datetime.now().isoformat()
    }


# --------------------------------------------------
# Predição de fraude
# --------------------------------------------------
@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """
    Endpoint principal para predição de fraude.

    Recebe uma transação, executa a inferência
    e retorna o resultado dos modelos e da decisão combinada.
    """
    try:
        result = predict_transaction(req.transaction.dict())
        return (result)

    except ValueError as ve:
        logger.error(f"Erro de validação: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.exception("Erro interno durante a predição")
        raise HTTPException(
            status_code=500,
            detail="Erro interno no processamento da predição"
        )
