# Fraud Sentinel 🛡️

Fraud Sentinel é uma **API de inferência em tempo real para detecção de fraudes em transações de cartão de crédito**, construída com **FastAPI** e um **ensemble de modelos de machine learning (XGBoost + Random Forest)**.

A aplicação foi projetada para operar em cenários de **streaming**, integrando-se facilmente a pipelines com **Kafka** e **Data Lake**, seguindo boas práticas de engenharia de software e MLOps.

---

## 🎯 Objetivo da Aplicação

- Receber transações financeiras em tempo real
- Executar inferência de fraude usando múltiplos modelos
- Combinar resultados via **ensemble**
- Retornar probabilidade de fraude, nível de risco e ação recomendada
- Produzir uma saída estruturada para persistência em Data Lake
- Suportar versionamento e rastreabilidade de modelos

---

## 🧠 Modelos de Machine Learning

- **XGBoost Classifier**
- **Random Forest Classifier**
- **Estratégia de Ensemble**: média simples das probabilidades

A decisão final de fraude é baseada na probabilidade combinada dos dois modelos.

---

## 📁 Estrutura da Aplicação

```plaintext
fraud_sentinel/
├── app/
│ ├── app.py # Factory do FastAPI
│ ├── routes.py # Rotas da API
│ ├── schemas.py # Schemas Pydantic (request/response)
│ ├── logging_config.py # Configuração de logs rotativos
│ ├── utils.py # Funções utilitárias
│ └── services/
│ ├── preprocessing.py # Feature engineering
│ ├── inference.py # Inferência e ensemble
│ └── artifacts.py # Carregamento de modelos
├── models/
│ ├── xgboost/
│ ├── random_forest/
│ └── preprocessor/
├── logs/
├── run.py # Bootstrap da aplicação
├── requirements.txt
└── README.md
```
> ⚠️ Os artefatos de modelo (`.pkl`, `metadata.json`) **não são versionados no Git**.  
Eles devem ser provisionados no deploy (ex: via MinIO).

---

## 🚀 Como Executar

### 1️⃣ Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Iniciar a aplicação
```bash
python run.py
```


A API ficará disponível em:

http://localhost:8000

---

## 📚 Documentação Automática

A aplicação expõe documentação automática via FastAPI:

- Swagger UI
http://localhost:8000/docs

- ReDoc
http://localhost:8000/redoc

---

## 📚 Documentação Automática

`POST /predict`

Executa a inferência de fraude para uma transação.

Exemplo de Request
```json
{
  "transaction": {
    "trans_num": "abc123",
    "amt": 999.99,
    "category": "grocery_net",
    "gender": "F",
    "state": "CA",
    "city_pop": 100000,
    "lat": 40.7128,
    "long": -74.0060,
    "merch_lat": 34.0522,
    "merch_long": -118.2437,
    "trans_date_trans_time": "2025-12-20T15:53:12",
    "dob": "1985-04-12"
  }
}
```

Exemplo de Response
```json
{
  "transaction_id": "abc123",
  "timestamp": "2025-12-20T21:10:20.426210",
  "models": {
    "xgboost": 0.4855,
    "random_forest": 0.0133
  },
  "ensemble": {
    "fraud_probability": 0.2494,
    "confidence": 0.7506,
    "is_fraud": false,
    "risk_level": "BAIXO",
    "recommended_action": "APROVAR TRANSAÇÃO"
  },
  "processing": {
    "processing_time_ms": 77.58
  },
  "metadata": {
    "request_id": "3f3a1f6c-8b6d-4b9b-8f2d-1e6c7e4c92a1",
    "status": "success"
  }
}
```

---

## 🧾 Logs

- Logs rotativos por tamanho

- Saída em arquivo e console

- Preparado para execução local e em container

Local padrão:
```bash
logs/fraud_sentinel.log
```

---

## 📦 Artefatos de Modelo

A aplicação espera os seguintes artefatos em tempo de execução:

- Modelo XGBoost (`.pkl`)

- Modelo Random Forest (`.pkl`)

- Preprocessor (`.pkl`)

- Metadados de cada artefato (`metadata.json`)

Esses arquivos são carregados no startup da aplicação.

---

## 🧠 Observações de Arquitetura

- API stateless

- Inferência síncrona (tempo real)

- Saída estruturada para persistência em Data Lake

- Compatível com arquiteturas Lambda (speed layer)

---

## 📦 Artefatos de Modelo

Este projeto possui caráter educacional (capstone), mas foi desenvolvido com padrões realistas de mercado, visando fácil evolução para ambientes produtivos.