from pydantic import BaseModel, Field
from typing import Optional, Dict


# --------------------------------------------------
# Schema da transação
# --------------------------------------------------
class Transaction(BaseModel):
    """
    Representa uma transação financeira a ser avaliada.
    Os campos refletem as features esperadas pelo modelo.
    """

    # Dados da transação
    trans_num: Optional[str] = Field(None, example="c85ca3d4fd1e42dc9571b0fa46708889")
    amt: float = Field(..., example=1074.22, description="Valor da transação")
    category: str = Field(..., example="shopping_pos")
    gender: str = Field(..., example="F")
    state: str = Field(..., example="CA")
    city_pop: int = Field(..., example=100000)

    # Localização
    lat: float = Field(..., example=40.7128)
    long: float = Field(..., example=-74.0060)
    merch_lat: float = Field(..., example=34.0522)
    merch_long: float = Field(..., example=-118.2437)

    # Datas 
    trans_date_trans_time: Optional[str] = Field(
        None,
        example="2025-12-20T15:53:12"
    )
    dob: Optional[str] = Field(
        None,
        example="1985-04-12"
    )


# --------------------------------------------------
# Request do endpoint /predict
# --------------------------------------------------
class PredictRequest(BaseModel):
    """
    Payload esperado pelo endpoint /predict
    """
    transaction: Transaction


# --------------------------------------------------
# Schemas de resposta
# --------------------------------------------------
class ModelScores(BaseModel):
    xgboost: float
    random_forest: float


class EnsembleResult(BaseModel):
    fraud_probability: float
    confidence: float
    is_fraud: bool
    risk_level: str
    recommended_action: str


class ModelInfo(BaseModel):
    strategy: str
    versions: Dict[str, str]
    preprocessor_version: Optional[str]


class ProcessingInfo(BaseModel):
    processing_time_ms: float


class Insights(BaseModel):
    transaction_value: Optional[float]
    location_distance_km: Optional[float]


class Metadata(BaseModel):
    request_id: str
    status: str


class PredictResponse(BaseModel):
    """
    Estrutura da resposta de predição (contrato oficial)
    """
    transaction_id: str
    timestamp: str

    models: ModelScores
    ensemble: EnsembleResult
    model: ModelInfo

    processing: ProcessingInfo
    insights: Optional[Insights]

    metadata: Metadata
