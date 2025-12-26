from pydantic import BaseModel
from typing import Any, Dict


class TransactionEvent(BaseModel):
    transaction: Dict[str, Any]


class ScoredEvent(BaseModel):
    transaction: Dict[str, Any]
    inference: Dict[str, Any]
