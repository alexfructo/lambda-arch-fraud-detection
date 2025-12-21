import logging
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict


logger = logging.getLogger("fraud_sentinel.preprocessing")

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
        # ENGENHARIA DE FEATURES 
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

