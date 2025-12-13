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

# 🤝 Como Contribuir

#### **1) Clone e prepare o ambiente**
```bash
git clone https://github.com/seuusuario/lambda-fraud-detection.git
cd lambda-fraud-detection
git checkout develop
git pull origin develop
```

#### **2) Crie sua branch de trabalho**
```bash
git checkout -b seu-nome/descricao-curta
# Exemplos:
# git checkout -b maria/novo-modelo-fraude
# git checkout -b joao/melhoria-dashboard
# git checkout -b pedro/correcao-kafka
```

#### **3) Configure o ambiente**
```bash
cp .env.example .env
docker-compose up -d
```

#### **4) Desenvolva e teste suas alterações**

- Modifique o código conforme necessário
- Teste com: `docker-compose restart <servico>`
- Verifique se tudo funciona com os containers

#### **5) Commit e envie suas mudanças**
```bash
git add .
git commit -m "feat: descrição clara do que foi feito"
# Exemplos:
# git commit -m "feat: adiciona novo modelo de detecção"
# git commit -m "fix: corrige conexão com MySQL"
git push origin sua-branch
```

#### **6) Crie um Pull Request (PR)**

1. Vá até o repositório no GitHub
2. Clique em "Pull Requests" → "New Pull Request"
3. Configure:
   - base: develop ← compare: sua-branch
4. Descreva o que foi feito e porquê
5. Aguarde revisão


### ✅ Checklist antes de criar PR

- Testei localmente com docker-compose up
- Meu código segue os padrões existentes
- Adicionei/atualizei documentação se necessário
- Não quebrei funcionalidades existentes
- Commits com mensagens descritivas

### 📌 Regras do Projeto

- Sempre trabalhe a partir da branch develop
- Crie PRs apenas para develop (não para main)
- Aguarde aprovação antes do merge
- Mantenha commits pequenos e descritivos
- Use português nas mensagens de commit (projeto acadêmico BR)
- Teste sempre com Docker antes de commitar

### 📝Convenções de commits
```bash
# Padrão recomendado:
git commit -m "feat: adiciona nova lambda de processamento"
git commit -m "fix: corrige bug no docker-compose"
git commit -m "docs: atualiza README com setup"
git commit -m "test: adiciona testes para ETL"
git commit -m "chore: atualiza versões do docker"

# Tipos úteis para seu projeto:
- feat: Nova funcionalidade
- fix: Correção de bug
- refactor: Refatoração sem mudança funcional
- perf: Melhorias de performance
- infra: Alterações na infraestrutura Docker
- data: Modificações em datasets/scripts de dados
```

---

# ▶️ Como Executar o Projeto

#### **2) Crie sua branch de trabalho**
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
