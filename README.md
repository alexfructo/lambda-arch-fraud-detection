# Detecção de Fraudes em Cartões de Crédito usando Arquitetura Lambda  
## Projeto Capstone – Engenharia de Dados

Este projeto implementa uma solução completa de **Engenharia de Dados** voltada para a **detecção de fraudes em transações de cartão de crédito**, utilizando uma **Arquitetura Lambda** composta por:

- **Speed Layer** (Kafka + processamento streaming)
- **Batch Layer** (Spark + Airflow)
- **Serving Layer** (MySQL + API FastAPI + Streamlit Dashboard)
- **Data Lake (MinIO)** com camadas **Bronze, Silver e Gold**
- **Feature Store** e **Model Store**

A solução foi construída com foco acadêmico, mas seguindo boas práticas reais usadas na indústria.

---

## 🏗️ Arquitetura Geral

A arquitetura Lambda implementada combina:

- **Processamento em lote (Batch)**  
  Agregações históricas, validações e padronizações usando Airflow + Spark.

- **Processamento em tempo real (Streaming)**  
  Consumidores Kafka aplicam transformações e realizam inferência imediata com Random Forest.

- **Serving Layer**  
  Os resultados são disponibilizados por uma API e consumidos por dashboards no Streamlit.

---

## 📦 Componentes da Solução

| Componente | Descrição |
|-----------|-----------|
| **Kafka + Zookeeper** | Ingestão contínua de transações de cartão (Speed Layer) |
| **MinIO** | Data Lake estruturado em Bronze / Silver / Gold |
| **MySQL** | Base de consulta rápida para servir visões agregadas |
| **Airflow** | Orquestração dos jobs batch |
| **Streamlit** | Dashboard para consumo dos dados |
| **API (FastAPI)** | Endpoint para servir inferências de fraude |
| **Gerador de Transações** | Microserviço que simula transações de cartão |
| **Modelo Random Forest** | Motor da inteligência de fraude |

---

## 📁 Estrutura do Repositório

```plaintext
lambda-fraud-detection/
|
├── apps/
│   ├── generator/
│   ├── api/
│   └── dashboard/
|
├── data/
│   ├── minio/
│   └── mysql/
|
├── infra/
│   ├── airflow/
│   ├── kafka/
│   └── minio/
|
├── .env-example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# 🛠️ Tecnologias Utilizadas

### **Infraestrutura**
- Docker & Docker Compose  
- Kafka, Zookeeper  
- MinIO (S3 compatível)  
- MySQL  
- Apache Airflow  

### **Processamento**
- Python  
- Apache Spark  
- Kafka Consumers / Producers  

### **Machine Learning**
- Scikit-learn  
- Random Forest  
- Feature Store simples (arquivos versionados)  
- Model Store (metadados + `.pkl`)  

### **Serviços**
- FastAPI  
- Streamlit  

---

# ▶️ Como Executar o Projeto

#### **1) Clone o repositório**
```bash
git clone https://github.com/seuusuario/lambda-fraud-detection.git
cd lambda-fraud-detection
```

#### **2) Copie o arquivo de variáveis de ambiente**
```bash
cp .env.example .env
```

#### **3) Suba toda a infraestrutura**
```bash
docker-compose up -d
```

Isso iniciará:

- Kafka + Zookeeper  
- MinIO (com buckets automáticos)  
- MySQL  
- Airflow  
- API FastAPI  
- Streamlit Dashboard  
- Gerador de transações  

---

#### **4) Acesse os serviços**

| Serviço | URL |
|--------|-----|
| Streamlit Dashboard | http://localhost:8501 |
| API FastAPI | http://localhost:8000/docs |
| Airflow | http://localhost:8080 |
| MinIO Console | http://localhost:9001 |
| MySQL | localhost:3306 |

---

# 🔄 Fluxo do Pipeline

### **Speed Layer**
- Gerador envia transações → Kafka  
- Consumer lê mensagem  
- Processamento + aplicação do modelo ML  
- Escrita no Data Lake (Silver / Gold)  
- Atualização da camada Serving (MySQL)  

### **Batch Layer**
- Airflow agenda o job  
- Spark processa dados históricos  
- Gera agregações → Silver / Gold  
- Atualiza Feature Store  

### **Serving Layer**
- API serve predições para sistemas externos  
- Dashboard consome dados consolidados  

---

# 📡 Endpoints da API

### **POST /predict**  
Retorna a probabilidade de fraude com base nos campos da transação.

### **GET /health**  
Valida se o serviço está operacional.

> Especificações completas em **docs/api_spec.yaml**

---

# 📚 Documentação Complementar

A pasta **docs/** contém:

- architecture.md – explicação detalhada da arquitetura  
- diagrams/ – diagramas da solução  
- data_dictionary.md – dicionário de dados  
- api_spec.yaml – documentação OpenAPI  

---

# 🚀 Melhorias Futuras

- 
---

# 👤 Autores

Projeto desenvolvido por Alex, Luiz, Marcos, Priscila e Yuri como parte do Capstone de Engenharia de Dados.
