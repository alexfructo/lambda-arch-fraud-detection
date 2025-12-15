# Transaction Generator

Gerador de transações sintéticas de cartão de crédito utilizado como fonte
de eventos para o pipeline de detecção de fraude.

## Objetivo

Simular transações financeiras em tempo quase real e publicá-las em um tópico Kafka,
permitindo testes de processamento, detecção de fraude e ingestão em data lake.

## Modos de execução

### Kafka (streaming)
Envia transações continuamente para um tópico Kafka.

```bash
python main.py --mode kafka
```

### CSV (batch)
Envia transações continuamente para um tópico Kafka.

```bash
python main.py --mode csv --total 1000 --output transactions.csv
```

### Print (debug)

Imprime transações no console.

```bash
python main.py --mode print
```

## Configuração

### .env

```bash
KAFKA_BOOTSTRAP=localhost:9092
KAFKA_TOPIC=transactions_raw
```

### config.json

```bash
{
  "transactions_per_second": 4,

  "min_amount": 1.0,
  "max_amount": 1200.0,

  "categories": [
    "shopping", "food", "travel", "gas", "entertainment",
    "online_services", "subscriptions", "electronics"
  ],

  "merchants": [
    "McDonalds", "Amazon", "Uber", "Shell", "Walmart",
    "Target", "Starbucks", "BestBuy", "Costco", "HomeDepot",
    "CVS Pharmacy", "Apple Store", "Delta Airlines",
    "Airbnb", "Spotify", "Netflix", "Burger King", "Subway"
  ],

  "states": [
    "CA", "NY", "TX", "FL", "WA", "NV", "IL", "NJ", "MA", "GA"
  ],

  "amount_distribution": "uniform",  
  "max_city_population": 5000000
}
```

## Dependências

- Kafka em execução
- Tópico Kafka previamente criado
