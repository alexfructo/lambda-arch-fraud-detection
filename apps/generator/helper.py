import json
from faker import Faker
import random

fake = Faker()

def generate_clients(n=5000):
    clients = []
    for i in range(n):
        clients.append({
            "client_id": f"C{i:05d}",
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace("\n", ", "),
            "age": random.randint(18, 80),
            "income": round(random.uniform(1500, 30000), 2),
            "risk_score": random.uniform(0, 1)  # pode usar depois para ajustar prob de fraude
        })
    return clients

def generate_merchants(n=1500):
    merchants = []
    categories = [
        "electronics", "clothing", "groceries", "restaurants", "travel",
        "gaming", "subscriptions", "luxury", "health", "services"
    ]

    for i in range(n):
        merchants.append({
            "merchant_id": f"M{i:05d}",
            "merchant_name": fake.company(),
            "category": random.choice(categories),
            "city": fake.city(),
            "country": fake.country(),
            "risk_score": random.uniform(0, 1),  # idem
        })
    return merchants


if __name__ == "__main__":
    clients = generate_clients(5000)
    merchants = generate_merchants(1500)

    with open("clients.json", "w") as f:
        json.dump(clients, f, indent=2)

    with open("merchants.json", "w") as f:
        json.dump(merchants, f, indent=2)

    print("Arquivos clients.json e merchants.json gerados com sucesso!")
