import uuid
import random
import json
from faker import Faker
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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

    def random_datetime_weighted(self, start: datetime, end: datetime, decay: float = 3.0) -> datetime:
        """
        Gera um datetime aleatório entre start e end,
        com maior concentração próximo de 'end'.

        decay:
            - quanto maior, mais transações recentes
            - 2.0  = leve
            - 3.0  = realista (recomendado)
            - 4.0+ = bem concentrado no presente
        """
    
        total_seconds = int((end - start).total_seconds())

        r = random.random()
        weighted = 1 - (r ** decay)

        random_seconds = int(weighted * total_seconds)
        return start + timedelta(seconds=random_seconds)

    def generate_transaction(self, months_back=6):
        """
        Gera uma transação de cartão de crédito com base nas configurações carregadas.
        Args:
            months_back (int): Quantidade de meses para gerar transações do passado até o presente.
        """
        
        end = datetime.now()
        start = end - relativedelta(months=months_back)

        trans_date = self.random_datetime_weighted(start, end)

        # merchant coordinates simulados próximos ao cliente
        base_merch_lat = float(fake.latitude())
        base_merch_long = float(fake.longitude())

        trans = {
            "trans_date_trans_time": trans_date.strftime("%Y-%m-%d %H:%M:%S"),
            "unix_time": int(trans_date.timestamp()),

            "cc_num": fake.credit_card_number(),
            "merchant": random.choice(self.config["merchants"]),
            "category": random.choice(self.config["categories"]),

            "amt": round(
                random.uniform(
                    self.config["min_amount"],
                    self.config["max_amount"]
                ), 2
            ),

            "first": fake.first_name(),
            "last": fake.last_name(),
            "gender": random.choice(["M", "F"]),

            "street": fake.street_address(),
            "city": fake.city(),
            "state": random.choice(self.config["states"]),
            "zip": fake.zipcode(),

            "lat": float(fake.latitude()),
            "long": float(fake.longitude()),

            "city_pop": random.randint(200, self.config.get("max_city_population", 5000000)),

            "job": fake.job(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d"),

            "trans_num": uuid.uuid4().hex,

            "merch_lat": base_merch_lat,
            "merch_long": base_merch_long
        }

        return trans
