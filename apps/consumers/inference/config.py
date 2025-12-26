import os
from dotenv import load_dotenv

# Caminho absoluto do .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path, override=True)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")

RAW_TOPIC = "transactions_raw"
SCORED_TOPIC = "transactions_scored"

GROUP_ID = "fraud-inference-consumer"

FRAUD_API_URL = os.getenv(
    "FRAUD_API_URL",
    "http://fraud-sentinel:8000/predict"
)

REQUEST_TIMEOUT = 5  # segundos
