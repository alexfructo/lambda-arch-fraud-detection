import json
import time
import logging
import requests

from confluent_kafka import Consumer, Producer, KafkaError
from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    RAW_TOPIC,
    SCORED_TOPIC,
    GROUP_ID,
    FRAUD_API_URL,
    REQUEST_TIMEOUT,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("fraud-inference-consumer")


def create_consumer() -> Consumer:
    return Consumer(
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "group.id": GROUP_ID,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }
    )


def create_producer() -> Producer:
    return Producer(
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        }
    )


def call_fraud_api(transaction: dict) -> dict:
    response = requests.post(
        FRAUD_API_URL,
        json={"transaction": transaction},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def main():
    consumer = create_consumer()
    producer = create_producer()

    consumer.subscribe([RAW_TOPIC])

    logger.info("Consumer iniciado. Aguardando mensagens...")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    logger.error(f"Erro Kafka: {msg.error()}")
                continue

            try:
                raw_event = json.loads(msg.value().decode("utf-8"))
                transaction = raw_event.get("transaction", raw_event)

                logger.info(
                    f"Processando transação {transaction.get('trans_num', 'unknown')}"
                )

                inference_result = call_fraud_api(transaction)

                enriched_event = {
                    "transaction": transaction,
                    "inference": inference_result,
                    "processed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }

                producer.produce(
                    SCORED_TOPIC,
                    key=str(transaction.get("trans_num")),
                    value=json.dumps(enriched_event).encode("utf-8"),
                )
                producer.flush()

                consumer.commit(msg)
                logger.info("Evento inferido e publicado com sucesso")

            except Exception as e:
                logger.exception(f"Erro ao processar mensagem: {e}")

    except KeyboardInterrupt:
        logger.info("Encerrando consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()
