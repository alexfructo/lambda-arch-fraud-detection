# XGBoost API
API desenvolvida em Flask para expor o modelo XGBoost treinado a partir do arquivo fraudTest.csv
## Componentes da API
| Componente | Descrição |
|------------|-----------|
| feature_names.pkl | Nome das Features utilizadas no modelo |
| fraud_detection_api.py | Implementação da API |
| preprocessor.pkl | Dados de preprocessamento para o modelo |
| requirements-api.txt | Requisitos dos imports e versões das bibliotecas utilizadas na API (devem ser compatíveis com o ambiente em que o modelo foi treinado) |
| xgboost_fraud_model.pkl | Modelo de predição de fraudes XGBoost |
## Endpoints da API
| Endpoint | Descrição |
|----------|-----------|
| @app.route('/') | Endpoint inicial para verificar se a API está funcionando |
| @app.route('/health', methods=['GET']) | Endpoint para verificar a saúde da API e dos modelos |
| @app.route('/model_info', methods=['GET']) | Endpoint para obter informações sobre o modelo |
| @app.route('/predict', methods=['POST']) | Endpoint principal para predição de fraude em tempo real |
| @app.route('/batch_predict', methods=['POST']) | Endpoint para predição em lote de múltiplas transações |
| @app.route('/validate', methods=['POST']) | Endpoint para validar o modelo com dados conhecidos (Útil para monitoramento de drift)|
## Erros HTTP Tratados
| Erro HTTP | Descrição |
|-----------|-----------|
| @app.errorhandler(404) | Endpoint não encontrado |
| @app.errorhandler(405) | Método não permitido |
| @app.errorhandler(500) | Erro interno do servidor |
## Exemplos de uso da predição
### Teste 1: Transação simples
``` bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction": {
        "amt": 100.0,
        "category": "grocery",
        "state": "NY",
        "city_pop": 8000000,
        "gender": "M",
        "dob": "1980-01-01",
        "trans_date_trans_time": "2024-01-15 14:30:00",
        "lat": 40.7128,
        "long": -74.0060,
        "merch_lat": 40.7589,
        "merch_long": -73.9851
    }
}'
```
### Saída do Teste 1
``` json
{
    "insights": {
        "location_distance_km": 5.4108119891801,
        "top_risk_factors": [
            "amt_log",
            "amt",
            "category_grocery_net"
        ],
        "transaction_value": 100.0
    },
    "metadata": {
        "request_id": "req_1766235299",
        "status": "success"
    },
    "model": {
        "type": "advanced",
        "version": "1.0.0"
    },
    "prediction": {
        "confidence": 0.9984,
        "fraud_probability": 0.0016,
        "is_fraud": false,
        "recommended_action": "APROVAR TRANSA\u00c7\u00c3O",
        "risk_level": "BAIXO"
    },
    "processing": {
        "features_used": 75,
        "processing_time_ms": 17.57
    },
    "timestamp": "2025-12-20T12:54:59.940306",
    "transaction_id": "unknown"
}
```
### Teste 2: Transação com mais dados
``` bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction": {
        "trans_date_trans_time": "2024-01-15 14:30:00",
        "category": "grocery_pos",
        "amt": 250.75,
        "gender": "F",
        "city_pop": 500000,
        "dob": "1990-05-20",
        "lat": 34.0522,
        "long": -118.2437,
        "merch_lat": 34.0736,
        "merch_long": -118.4004,
        "state": "CA"
    }
}'
```
### Saída do Teste 2:
``` json
{
    "insights": {
        "location_distance_km": 14.605620747519426,
        "top_risk_factors": [
            "amt_log",
            "amt",
            "category_grocery_net"
        ],
        "transaction_value": 250.75
    },
    "metadata": {
        "request_id": "req_1766235170",
        "status": "success"
    },
    "model": {
        "type": "advanced",
        "version": "1.0.0"
    },
    "prediction": {
        "confidence": 0.9828,
        "fraud_probability": 0.0172,
        "is_fraud": false,
        "recommended_action": "APROVAR TRANSA\u00c7\u00c3O",
        "risk_level": "BAIXO"
    },
    "processing": {
        "features_used": 75,
        "processing_time_ms": 15.36
    },
    "timestamp": "2025-12-20T12:52:50.656061",
    "transaction_id": "unknown"
}
```
### Teste 3: Batch prediction
``` bash
curl -X POST http://localhost:5000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
        {
            "amt": 50.0,
            "category": "grocery",
            "state": "NY",
            "city_pop": 8000000,
            "gender": "M"
        },
        {
            "amt": 1200.0,
            "category": "shopping",
            "state": "FL",
            "city_pop": 200000,
            "gender": "F"
        }
    ]
}'
```
### Saída do Teste 3
```json
{
    "avg_processing_time_ms": 7.85,
    "batch_id": "batch_1766234617",
    "failed_predictions": 0,
    "fraud_count": 0,
    "fraud_percentage": 0.0,
    "results": [
        {
            "fraud_probability": 0.0007,
            "is_fraud": false,
            "processing_time_ms": 8.84,
            "status": "success",
            "transaction_id": "trans_0"
        },
        {
            "fraud_probability": 0.1288,
            "is_fraud": false,
            "processing_time_ms": 6.86,
            "status": "success",
            "transaction_id": "trans_1"
        }
    ],
    "successful_predictions": 2,
    "timestamp": "2025-12-20T12:43:37.561109",
    "total_transactions": 2
}

```

## TODO:
Avaliar thresolds implementados no endpoint /predict 
```python
        # Determinar nível de risco
        if fraud_probability >= 0.8:
            risk_level = "CRÍTICO"
            action = "BLOQUEAR TRANSAÇÃO"
        elif fraud_probability >= 0.6:
            risk_level = "ALTO"
            action = "SOLICITAR AUTENTICAÇÃO ADICIONAL"
        elif fraud_probability >= 0.4:
            risk_level = "MÉDIO"
            action = "MONITORAR COMPORTAMENTO"
        else:
            risk_level = "BAIXO"
            action = "APROVAR TRANSAÇÃO"
```