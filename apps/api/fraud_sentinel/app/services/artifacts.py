import json
import joblib
import logging
from pathlib import Path

logger = logging.getLogger("fraud_sentinel.artifacts")


def load_pickle(path: Path, critical: bool = True):
    if not path.exists():
        msg = f"Artefato não encontrado: {path}"
        if critical:
            logger.error(msg)
            raise FileNotFoundError(msg)
        logger.warning(msg)
        return None

    try:
        return joblib.load(path)
    except Exception as e:
        msg = f"Erro ao carregar artefato {path}: {e}"
        logger.error(msg)
        if critical:
            raise
        return None


def load_metadata(path: Path) -> dict:
    if not path.exists():
        logger.warning(f"Metadata não encontrada: {path}")
        return {
            "version": "unknown",
            "trained_at": None
        }

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Erro ao ler metadata {path}: {e}")
        return {
            "version": "unknown",
            "trained_at": None
        }
