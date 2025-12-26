# Consumer de Transações, Inferência de Fraude e Producer de Pontuação de Fraude

Este serviço é responsável por consumir transações brutas publicadas no Kafka,
realizar a inferência de fraude chamando a API **Fraud Sentinel** e publicar o
resultado no tópico `transactions_scored`.

Ele representa a **camada de inferência em tempo real** da arquitetura Lambda.

---

## 📌 Responsabilidade

- Consumir mensagens do tópico Kafka `transactions_raw`
- Enviar a transação para a API de inferência (`fraud-sentinel`)
- Receber o resultado da predição (fraude ou não)
- Publicar o evento enriquecido no tópico `transactions_scored`

---

## 🔁 Fluxo de Dados

```text
Kafka (transactions_raw)
        |
        v
Consumer Inference
        |
        v
Fraud Sentinel API (/predict)
        |
        v
Kafka (transactions_scored)
```

---

## ⚙️ Configuração via Variáveis de Ambiente

|Variável |	Descrição |
| ----------- | ----------- |
| KAFKA_BOOTSTRAP | Endereço do broker Kafka |
| FRAUD_API_URL | URL da API Fraud Sentinel |

---

## ▶️ Execução

Local (exemplo)
```bash
python main.py
```

Docker (via docker-compose)
```yml
consumer-inference:
  build: ./apps/consumers/inference
  command: python main.py
```

