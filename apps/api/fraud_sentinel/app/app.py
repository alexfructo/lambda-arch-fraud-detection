import logging
from fastapi import FastAPI
from app.routes import router
from app.logging_config import setup_logging

# --------------------------------------------------
# Configuração básica de logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("fraud_sentinel.app")


# --------------------------------------------------
# Application Factory
# --------------------------------------------------
def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.

    Returns:
        FastAPI: aplicação configurada
    """
    logger = setup_logging()
    app = FastAPI(
        title="Fraud Sentinel API",
        description=(
            "API de detecção de fraudes em transações financeiras "
            "utilizando modelos de Machine Learning e decisão combinada."
        ),
        version="1.0.0"
    )

    # --------------------------------------------------
    # Registro das rotas
    # --------------------------------------------------
    app.include_router(router)

    return app
