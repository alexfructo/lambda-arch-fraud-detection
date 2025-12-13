import uuid
import time
import random
import json
from faker import Faker
from datetime import datetime

fake = Faker()

class TransactionGenerator:
    """
    Classe responsável por gerar transações simuladas de cartão de crédito.
    Os valores e listas de merchants/categorias/estados são carregados do config.json.

    O objetivo é manter a estrutura simples, mas permitir parametrização via arquivo.
    """

    def __init__(self, config_path="config.json"):
        """
        Inicializa o gerador carregando as configurações definidas pelo usuário.

        Args:
            config_path (str): Caminho para o arquivo JSON contendo as configurações.
        """
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def generate_transaction(self):
        """
        Gera uma transação única contendo dados como localização, merchant,
        categoria, valor e informações do portador do cartão.

        Returns:
            dict: Dicionário contendo todos os campos da transação.
        """

        now = datetime.now()

        # merchant coordinates simulados próximos ao cliente
        base_merch_lat = float(fake.latitude())
        base_merch_long = float(fake.longitude())

        trans = {
            # data/hora da transação
            "trans_date_trans_time": now.strftime("%Y-%m-%d %H:%M:%S"),

            # dados do cartão
            "cc_num": fake.credit_card_number(),

            # merchant e categoria (carregados do config.json)
            "merchant": random.choice(self.config["merchants"]),
            "category": random.choice(self.config["categories"]),

            # valor da transação
            "amt": round(
                random.uniform(
                    self.config["min_amount"],
                    self.config["max_amount"]
                ),
                2
            ),

            # dados pessoais básicos
            "first": fake.first_name(),
            "last": fake.last_name(),
            "gender": random.choice(["M", "F"]),

            # endereço
            "street": fake.street_address(),
            "city": fake.city(),
            "state": random.choice(self.config["states"]),
            "zip": fake.zipcode(),

            # geolocalização do cliente
            "lat": float(fake.latitude()),
            "long": float(fake.longitude()),

            # população da cidade (parametrizável)
            "city_pop": random.randint(200, self.config.get("max_city_population", 5000000)),

            # ocupação e data de nascimento
            "job": fake.job(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d"),

            # id único da transação
            "trans_num": uuid.uuid4().hex,

            # timestamp bruto
            "unix_time": int(time.time()),

            # localização aleatória do estabelecimento
            "merch_lat": base_merch_lat,
            "merch_long": base_merch_long
        }

        return trans
