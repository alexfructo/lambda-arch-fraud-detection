import argparse
import logging

from config import *
from mysql_client import create_mysql_connection
from kafka_client import create_consumer
from minio_client import create_minio_client
from writer_bronze import write_bronze
from writer_silver import write_silver
from writer_transactional import write_transactional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("fraud-consumer")

def main(mode: str):
    logger.info(f"Iniciando consumer no modo: {mode}")

    minio = create_minio_client(
        MINIO_ENDPOINT,
        MINIO_ACCESS_KEY,
        MINIO_SECRET_KEY
    )

    if mode == "raw":
        consumer = create_consumer(
            TOPIC_RAW,
            KAFKA_GROUP_RAW,
            KAFKA_BOOTSTRAP
        )

        for msg in consumer:
            write_bronze(minio, BRONZE_BUCKET, msg.value)
            logger.info("Evento raw persistido na bronze")

    elif mode == "scored":
        consumer = create_consumer(
            TOPIC_SCORED,
            KAFKA_GROUP_SCORED,
            KAFKA_BOOTSTRAP
        )

        mysql_conn = create_mysql_connection(
            MYSQL_HOST,
            MYSQL_DATABASE,
            MYSQL_USER,
            MYSQL_PASSWORD
        )

        for msg in consumer:
            write_silver(minio, SILVER_BUCKET, msg.value)
            write_transactional(mysql_conn, msg.value)
            logger.info("Evento scored persistido (silver + mysql)")

    else:
        raise ValueError("Modo inválido. Use raw ou scored.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["raw", "scored"])
    args = parser.parse_args()

    main(args.mode)
