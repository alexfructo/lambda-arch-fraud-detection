import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    logger = logging.getLogger("fraud_sentinel")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Log em arquivo com rotação
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,            # mantém 5 arquivos antigos
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Log no console (bom para dev / docker)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Evitar duplicação
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
