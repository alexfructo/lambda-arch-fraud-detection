# Consumer de Persistência

Este serviço é responsável por **persistir eventos de transações** provenientes do Kafka, atuando como parte da **camada de persistência da arquitetura Lambda** do projeto.

Ele suporta dois modos de execução distintos, controlados por argumento de inicialização:

- **raw** → persiste transações brutas na camada **Bronze** do Data Lake (MinIO)
- **scored** → persiste transações inferidas na camada **Silver** (MinIO) **e** em uma base **transacional MySQL**

---

## 📌 Visão Geral da Arquitetura

```text
Kafka
├── transactions_raw
│ └── consumer (mode=raw)
│ └── MinIO (Bronze)
│
└── transactions_scored
└── consumer (mode=scored)
├── MinIO (Silver)
└── MySQL (Base Transacional)
```


Este design permite:
- Separação clara de responsabilidades
- Escalabilidade independente por tipo de processamento
- Evolução futura para novos destinos (Gold, Feature Store, etc.)

---

## ⚙️ Modos de Execução

### 🔹 Modo `raw`
- Consome o tópico: `transactions_raw`
- Persiste eventos **sem transformação**
- Destino: **MinIO – bucket Bronze**
- Organização por partições de data

```bash
python main.py --mode raw
```
### 🔹 Modo scored

- Consome o tópico: transactions_scored

- Persiste:

    - Evento completo no **MinIO – bucket Silver**

    - Campos relevantes em **MySQL** (consulta transacional)

- Utilizado para auditoria, dashboards e análises rápidas

```bash
python main.py --mode scored
```

---

## 🗂️ Estrutura de Persistência

### Bronze (Raw)

```text
bronze/
└── transactions/
    └── raw/
        └── year=YYYY/month=MM/day=DD/
            └── <transaction_id>.json
```

### Silver (Scored)

```text
silver/
└── transactions/
    └── scored/
        └── year=YYYY/month=MM/day=DD/
            └── <transaction_id>.json
```

### MySQL (Transacional)

Tabela: transactions_scored

Campos incluem:

- Identificação da transação

- Probabilidade de fraude

- Decisão do ensemble

- Metadados dos modelos

- Métricas operacionais (tempo, status)

---

## 🔐 Configuração via Variáveis de Ambiente

### Kafka

- KAFKA_BOOTSTRAP

- TOPIC_RAW

- TOPIC_SCORED

- KAFKA_GROUP_RAW

- KAFKA_GROUP_SCORED

### MinIO

- MINIO_ENDPOINT

- MINIO_ACCESS_KEY

- MINIO_SECRET_KEY

- BRONZE_BUCKET

- SILVER_BUCKET

### MySQL (modo scored)

- MYSQL_HOST

- MYSQL_DATABASE

- MYSQL_USER

- MYSQL_PASSWORD

## 🧱 Estrutura do Projeto

```bash
persistence/
├── main.py
├── config.py
├── kafka_client.py
├── minio_client.py
├── writer_bronze.py
├── writer_silver.py
├── writer_transactional.py
├── requirements.txt
└── README.md
```