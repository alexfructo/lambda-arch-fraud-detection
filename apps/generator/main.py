import os
import time
import argparse
import logging
import csv
import json
from dotenv import load_dotenv
#from kafka import KafkaProducer

from generator import TransactionGenerator

# --------------------------------------------------------------
# CONFIGURA LOGGER
# --------------------------------------------------------------
def setup_logger():
    """
    Configura o logger padrão da aplicação.

    Retorna:
        logging.Logger: instância configurada do logger.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s",
    )
    return logging.getLogger("transaction_app")

logger = setup_logger()

# --------------------------------------------------------------
# MODO: GERAR ARQUIVO CSV
# --------------------------------------------------------------
def run_csv(gen: TransactionGenerator, total: int, output_file: str):
    """
    Gera um número fixo de transações e salva em um arquivo CSV.

    Args:
        gen (TransactionGenerator): Gerador de transações.
        total (int): Quantidade de transações a serem criadas.
        output_file (str): Nome/path do arquivo CSV de saída.
    """
    logger.info(f"Gerando {total} transações e salvando em {output_file}")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = None

        for _ in range(total):
            trans = gen.generate_transaction()

            # Inicializa o writer no primeiro registro (pega dinamicamente as colunas)
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=trans.keys())
                writer.writeheader()

            writer.writerow(trans)

    logger.info("Arquivo CSV gerado com sucesso.")

# --------------------------------------------------------------
# MODO: ENVIAR PARA KAFKA (mock)
# --------------------------------------------------------------
def run_kafka(gen: TransactionGenerator):

    bootstrap = os.getenv("KAFKA_BOOTSTRAP")
    topic = os.getenv("KAFKA_TOPIC")
    security = os.getenv("KAFKA_SECURITY", "PLAINTEXT")
    sasl_mech = os.getenv("KAFKA_SASL_MECH", "PLAIN")
    username = os.getenv("KAFKA_USERNAME")
    password = os.getenv("KAFKA_PASSWORD")

    logger.info(f"Enviando transações para Kafka — tópico: {topic}")

    kafka_config = {
        "bootstrap_servers": bootstrap,
        "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
        "security_protocol": security
    }

    # Se estiver usando SASL
    if username and password:
        kafka_config.update({
            "sasl_mechanism": sasl_mech,
            "sasl_plain_username": username,
            "sasl_plain_password": password,
        })

    producer = KafkaProducer(**kafka_config)

    tps = gen.config["transactions_per_second"]
    delay = 1 / tps

    while True:
        trans = gen.generate_transaction()
        producer.send(topic, value=trans)
        logger.info(f"Transação enviada: {trans['trans_num']}")
        time.sleep(delay)

# --------------------------------------------------------------
# MODO: PRINT (debug)
# --------------------------------------------------------------
def run_print(gen: TransactionGenerator):
    """
    Exibe transações no console continuamente, respeitando a taxa
    de transações por segundo definida em config.json.

    Args:
        gen (TransactionGenerator): Gerador de transações.
    """
    tps = gen.config["transactions_per_second"]
    delay = 1 / tps

    logger.info(f"Gerando {tps} transações por segundo...")

    while True:
        trans = gen.generate_transaction()
        logger.info(trans)
        time.sleep(delay)

# --------------------------------------------------------------
# MAIN
# --------------------------------------------------------------
def main():
    """
    Ponto de entrada da aplicação.

    A aplicação suporta três modos:
        --mode csv   → Gera um arquivo CSV com N transações
        --mode kafka → Envia transações continuamente para um tópico Kafka
        --mode print → Apenas imprime as transações no terminal

    Os parâmetros adicionais variam conforme o modo escolhido.
    """
    parser = argparse.ArgumentParser(description="Gerador de Transações de Cartão")

    parser.add_argument(
        "--mode",
        required=True,
        choices=["csv", "kafka", "print"],
        help="Modo de execução do gerador"
    )

    parser.add_argument(
        "--total",
        type=int,
        default=1000,
        help="Quantidade de transações (apenas no modo CSV)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="transactions.csv",
        help="Arquivo de saída CSV"
    )


    args = parser.parse_args()

    # Caminho absoluto do .env
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path, override=True)

    # Caminho absoluto do config.json
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    gen = TransactionGenerator(config_path=config_path)

    # Roteia para o modo escolhido
    if args.mode == "csv":
        run_csv(gen, args.total, args.output)

    elif args.mode == "kafka":
        run_kafka(gen)

    elif args.mode == "print":
        run_print(gen)


if __name__ == "__main__":
    main()
