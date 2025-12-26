import os
from dotenv import load_dotenv

# Caminho absoluto do .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path, override=True)

# Kafka
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
KAFKA_GROUP_RAW = os.getenv("KAFKA_GROUP_RAW", "transactions-raw-consumer")
KAFKA_GROUP_SCORED = os.getenv("KAFKA_GROUP_SCORED", "transactions-scored-consumer")

TOPIC_RAW = "transactions_raw"
TOPIC_SCORED = "transactions_scored"

# MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

BRONZE_BUCKET = "bronze"
SILVER_BUCKET = "silver"

# MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
