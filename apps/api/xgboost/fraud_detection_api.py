"""
API Flask para expor modelo XGBoost de detecção de fraudes financeiras
Arquivo: fraud_detection_api.py
"""

# ============================================
# 1. IMPORTAÇÕES
# ============================================
import json
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from datetime import datetime
import logging
from typing import Dict, List, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# 2. CONFIGURAÇÃO DA API FLASK
# ============================================
app = Flask(__name__)
CORS(app)  # Habilitar CORS para requisições de diferentes origens

# ============================================
# 3. CARREGAMENTO DOS MODELOS E PRÉ-PROCESSADORES
# ============================================
print("=" * 50)
print("CARREGANDO MODELOS E RECURSOS...")
print("=" * 50)

try:
    # Carregar modelo XGBoost treinado
    model = joblib.load('xgboost_fraud_model.pkl')
    print("✓ Modelo XGBoost carregado com sucesso")
    
    # Carregar preprocessor (StandardScaler + OneHotEncoder)
    preprocessor = joblib.load('preprocessor.pkl')
    print("✓ Pré-processador carregado com sucesso")
    
    # Carregar nomes das features
    with open('feature_names.pkl', 'rb') as f:
        feature_names = joblib.load(f)
    print(f"✓ {len(feature_names)} nomes de features carregados")
    
    # Carregar modelo simplificado como fallback
    # model_simple = joblib.load('xgboost_fraud_model_simple.pkl')
    # print("✓ Modelo simplificado carregado (fallback)")
    
    print("\n✅ TODOS OS RECURSOS CARREGADOS COM SUCESSO!")
    
except Exception as e:
    print(f"❌ ERRO AO CARREGAR MODELOS: {str(e)}")
    raise

# ============================================
# 4. FUNÇÕES AUXILIARES PARA PROCESSAMENTO
# ============================================
def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula distância aproximada em km entre duas coordenadas geográficas
    
    Args:
        lat1, lon1: Latitude e longitude do cliente
        lat2, lon2: Latitude e longitude do comerciante
    
    Returns:
        Distância em quilômetros
    """
    # Aproximação planar (suficiente para detecção de fraudes)
    dx = (lat2 - lat1) * 111  # 1 grau de latitude ≈ 111 km
    dy = (lon2 - lon1) * 111 * np.cos(np.radians(lat1))
    return np.sqrt(dx**2 + dy**2)

def criar_features_transacao(dados_transacao: Dict) -> pd.DataFrame:
    """
    Cria DataFrame com features processadas a partir dos dados brutos
    
    Args:
        dados_transacao: Dicionário com dados da transação
    
    Returns:
        DataFrame com features prontas para predição
    """
    try:
        # Criar DataFrame com uma única linha
        df = pd.DataFrame([dados_transacao])
        
        # ============================================
        # ENGENHARIA DE FEATURES (igual ao treinamento)
        # ============================================
        
        # 1. Converter datas
        if 'trans_date_trans_time' in df.columns:
            df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
            df['hora'] = df['trans_date_trans_time'].dt.hour
            df['dia_semana'] = df['trans_date_trans_time'].dt.dayofweek
            df['dia_mes'] = df['trans_date_trans_time'].dt.day
            df['mes'] = df['trans_date_trans_time'].dt.month
        
        # 2. Calcular idade se data de nascimento fornecida
        if 'dob' in df.columns and 'trans_date_trans_time' in df.columns:
            df['dob'] = pd.to_datetime(df['dob'])
            df['idade'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365
        
        # 3. Calcular distância entre cliente e comerciante
        if all(col in df.columns for col in ['lat', 'long', 'merch_lat', 'merch_long']):
            df['distancia_km'] = calcular_distancia(
                df['lat'].iloc[0], df['long'].iloc[0],
                df['merch_lat'].iloc[0], df['merch_long'].iloc[0]
            )
        
        # 4. Transformação logarítmica do valor
        if 'amt' in df.columns:
            df['amt_log'] = np.log1p(df['amt'])
        
        # 5. Garantir que todas as features necessárias existam
        features_esperadas = [
            'amt', 'amt_log', 'city_pop', 'idade', 'distancia_km',
            'hora', 'dia_semana', 'dia_mes', 'mes',
            'category', 'gender', 'state'
        ]
        
        # Adicionar valores padrão para features faltantes
        for feature in features_esperadas:
            if feature not in df.columns:
                if feature in ['amt_log', 'distancia_km', 'idade']:
                    df[feature] = 0  # Valores numéricos padrão
                elif feature in ['hora', 'dia_semana', 'dia_mes', 'mes']:
                    # Usar valores da data/hora atual se não fornecidos
                    now = datetime.now()
                    if feature == 'hora':
                        df[feature] = now.hour
                    elif feature == 'dia_semana':
                        df[feature] = now.weekday()
                    elif feature == 'dia_mes':
                        df[feature] = now.day
                    elif feature == 'mes':
                        df[feature] = now.month
                elif feature in ['city_pop']:
                    df[feature] = 100000  # População média padrão
                else:
                    df[feature] = 'unknown'  # Categóricas desconhecidas
        
        # Selecionar apenas as features na ordem esperada
        df_processed = df[features_esperadas].copy()
        
        return df_processed
        
    except Exception as e:
        logger.error(f"Erro ao criar features: {str(e)}")
        raise
# ============================================
# FUNÇÃO AUXILIAR: Converter tipos NumPy para Python nativo
# ============================================
def convert_to_python_types(obj):
    """
    Converte tipos NumPy (int64, float64, etc.) para tipos Python nativos
    para serialização JSON.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (list, tuple)):
        return [convert_to_python_types(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_to_python_types(value) for key, value in obj.items()}
    else:
        return obj

# ============================================
# 5. ROTAS DA API
# ============================================
@app.route('/')
def home():
    """Endpoint inicial para verificar se a API está funcionando"""
    return jsonify({
        'status': 'online',
        'service': 'Fraud Detection API',
        'version': '1.0.0',
        'model': 'XGBoost for Financial Fraud Detection',
        'endpoints': {
            '/predict': 'POST - Realizar predição de fraude',
            '/batch_predict': 'POST - Predição em lote',
            '/health': 'GET - Verificar saúde da API',
            '/model_info': 'GET - Informações do modelo'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar a saúde da API e dos modelos"""
    try:
        # Verificar se modelo está carregado
        model_score = 0.5  # Simulação de score do modelo
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'model_loaded': True,
            'preprocessor_loaded': True,
            'model_score': model_score
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Endpoint para obter informações sobre o modelo"""
    try:
        info = {
            'model_type': 'XGBoost Classifier',
            'n_features': len(feature_names) if 'feature_names' in locals() else 'unknown',
            'training_date': '2024-01-01',  # Data fictícia, em produção use metadados reais
            'performance': {
                'roc_auc': 0.95,  # Valores de exemplo
                'precision': 0.92,
                'recall': 0.88,
                'f1_score': 0.90
            },
            'features_importance_top_10': feature_names[:10] if 'feature_names' in locals() else []
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint principal para predição de fraude em tempo real
    """
    try:
        # Registrar início da predição
        start_time = datetime.now()
        logger.info(f"Predição iniciada: {start_time}")
        
        # Obter dados da requisição
        data = request.get_json()
        
        if not data or 'transaction' not in data:
            return jsonify({
                'error': 'Dados inválidos. Envie um JSON com a chave "transaction"'
            }), 400
        
        # Extrair dados da transação
        transaction_data = data['transaction']
        
        # Escolher modelo baseado no parâmetro (fallback para avançado)
        model_type = data.get('model_type', 'advanced')
        selected_model = model #if model_type == 'advanced' else model_simple
        
        # ============================================
        # PROCESSAMENTO DA TRANSAÇÃO
        # ============================================
        
        # 1. Criar features a partir dos dados brutos
        logger.info("Criando features da transação...")
        features_df = criar_features_transacao(transaction_data)
        
        # 2. Aplicar pré-processamento (normalização + one-hot encoding)
        logger.info("Aplicando pré-processamento...")
        features_processed = preprocessor.transform(features_df)
        
        # 3. Fazer predição
        logger.info("Realizando predição...")
        prediction = selected_model.predict(features_processed)[0]
        prediction_proba = selected_model.predict_proba(features_processed)[0]
        
        # 4. Calcular tempo de processamento
        processing_time = (datetime.now() - start_time).total_seconds() * 1000  # ms
        
        # ============================================
        # CONSTRUIR RESPOSTA (COM CONVERSÃO DE TIPOS)
        # ============================================
        
        # Interpretar predição (converter tipos NumPy)
        is_fraud = bool(prediction == 1)
        fraud_probability = float(prediction_proba[1])  # Converter para float Python
        
        confidence = fraud_probability if is_fraud else 1 - fraud_probability
        
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
        
        # Features mais importantes para esta predição
        top_features = []
        if hasattr(selected_model, 'feature_importances_'):
            importances = selected_model.feature_importances_
            top_indices = np.argsort(importances)[-3:][::-1]  # Top 3
            if 'feature_names' in globals():
                top_features = [feature_names[i] for i in top_indices]
        
        # Construir dicionário de resposta
        response_dict = {
            'transaction_id': transaction_data.get('trans_num', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'prediction': {
                'is_fraud': is_fraud,
                'fraud_probability': fraud_probability,  # Já é float Python
                'confidence': confidence,
                'risk_level': risk_level,
                'recommended_action': action
            },
            'model': {
                'type': model_type,
                'version': '1.0.0'
            },
            'processing': {
                'processing_time_ms': processing_time,
                'features_used': len(feature_names) if 'feature_names' in globals() else 0
            },
            'insights': {
                'top_risk_factors': top_features,
                'transaction_value': float(transaction_data.get('amt', 0)),
                'location_distance_km': float(features_df['distancia_km'].iloc[0]) if 'distancia_km' in features_df.columns else 0.0
            },
            'metadata': {
                'request_id': f"req_{int(datetime.now().timestamp())}",
                'status': 'success'
            }
        }
        
        # CONVERTER TODOS OS TYPES NUMPY PARA PYTHON NATIVO
        response_converted = convert_to_python_types(response_dict)
        
        # Arredondar valores decimais para melhor legibilidade
        if 'prediction' in response_converted:
            response_converted['prediction']['fraud_probability'] = round(
                response_converted['prediction']['fraud_probability'], 4
            )
            response_converted['prediction']['confidence'] = round(
                response_converted['prediction']['confidence'], 4
            )
        
        if 'processing' in response_converted:
            response_converted['processing']['processing_time_ms'] = round(
                response_converted['processing']['processing_time_ms'], 2
            )
        
        logger.info(f"Predição concluída: {is_fraud} (prob: {fraud_probability:.2%})")
        
        return jsonify(response_converted), 200
        
    except Exception as e:
        logger.error(f"Erro na predição: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': 'Erro interno no processamento',
            'details': str(e),
            'timestamp': datetime.now().isoformat(),
            'status': 'error'
        }), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Endpoint para predição em lote de múltiplas transações
    """
    try:
        data = request.get_json()
        
        if not data or 'transactions' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        transactions = data['transactions']
        model_type = data.get('model_type', 'advanced')
        selected_model = model #if model_type == 'advanced' else model_simple
        
        results = []
        processing_times = []
        
        for i, transaction_data in enumerate(transactions):
            start_time = datetime.now()
            
            try:
                # Processar cada transação
                features_df = criar_features_transacao(transaction_data)
                features_processed = preprocessor.transform(features_df)
                
                prediction = selected_model.predict(features_processed)[0]
                prediction_proba = selected_model.predict_proba(features_processed)[0]
                
                is_fraud = bool(prediction == 1)
                fraud_probability = float(prediction_proba[1])  # Converter para float
                
                processing_time = (datetime.now() - start_time).total_seconds() * 1000
                processing_times.append(processing_time)
                
                # Converter valores NumPy para Python
                result = {
                    'transaction_id': transaction_data.get('trans_num', f'trans_{i}'),
                    'is_fraud': is_fraud,
                    'fraud_probability': round(fraud_probability, 4),
                    'processing_time_ms': round(float(processing_time), 2),
                    'status': 'success'
                }
                
                results.append(convert_to_python_types(result))
                
            except Exception as e:
                results.append({
                    'transaction_id': transaction_data.get('trans_num', f'trans_{i}'),
                    'error': str(e),
                    'status': 'error'
                })
        
        # Estatísticas do batch
        avg_processing_time = np.mean(processing_times) if processing_times else 0
        fraud_count = sum(1 for r in results if r.get('is_fraud', False))
        
        response = {
            'batch_id': f"batch_{int(datetime.now().timestamp())}",
            'total_transactions': len(transactions),
            'successful_predictions': sum(1 for r in results if r['status'] == 'success'),
            'failed_predictions': sum(1 for r in results if r['status'] == 'error'),
            'fraud_count': int(fraud_count),  # Converter para int
            'fraud_percentage': round(float(fraud_count) / len(results) * 100, 2) if results else 0,
            'avg_processing_time_ms': round(float(avg_processing_time), 2),
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(convert_to_python_types(response)), 200
        
    except Exception as e:
        logger.error(f"Erro no batch prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/validate', methods=['POST'])
def validate_model():
    """
    Endpoint para validar o modelo com dados conhecidos
    (Útil para monitoramento de drift)
    """
    try:
        data = request.get_json()
        
        # Dados de validação devem conter features e labels
        if 'X_test' not in data or 'y_test' not in data:
            return jsonify({'error': 'Forneça X_test e y_test'}), 400
        
        # Aqui em produção você calcularia métricas reais
        # Para exemplo, retornamos métricas simuladas
        
        return jsonify({
            'validation_results': {
                'accuracy': 0.95,
                'precision': 0.92,
                'recall': 0.88,
                'f1_score': 0.90,
                'roc_auc': 0.96,
                'timestamp': datetime.now().isoformat()
            },
            'model_status': 'healthy',
            'drift_detected': False
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# 6. MANIPULADORES DE ERRO
# ============================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método não permitido'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Erro interno do servidor',
        'timestamp': datetime.now().isoformat()
    }), 500

# ============================================
# 7. CONFIGURAÇÃO E INICIALIZAÇÃO
# ============================================
if __name__ == '__main__':
    # Configurações para produção
    host = '0.0.0.0'  # Acessível externamente
    port = 5000
    debug = False  # False em produção!
    
    print("\n" + "=" * 50)
    print("INICIANDO API DE DETECÇÃO DE FRAUDES")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print("\nEndpoints disponíveis:")
    print(f"  http://{host}:{port}/")
    print(f"  http://{host}:{port}/predict (POST)")
    print(f"  http://{host}:{port}/health (GET)")
    print(f"  http://{host}:{port}/model_info (GET)")
    print("\n✅ API PRONTA PARA REQUISIÇÕES")
    print("=" * 50)
    
    # Iniciar servidor Flask
    app.run(host=host, port=port, debug=debug)