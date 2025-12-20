# Use uma imagem Python oficial mais leve
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# 1. ATUALIZAR E INSTALAR DEPENDÊNCIAS DO SISTEMA
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. COPIAR E INSTALAR DEPENDÊNCIAS PYTHON PRIMEIRO
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# 3. VERIFICAR SE GUNICORN FOI INSTALADO
RUN python -c "import gunicorn; print('Gunicorn instalado:', gunicorn.__version__)"

# 4. COPIAR CÓDIGO FONTE E MODELOS
COPY fraud_detection_api.py .
COPY xgboost_fraud_model.pkl .
COPY preprocessor.pkl .
COPY feature_names.pkl .

# 5. CRIAR DIRETÓRIO DE LOGS
RUN mkdir -p /app/logs

# 6. VERIFICAR PATH DO PYTHON
RUN echo "Python path:" && python -c "import sys; print(sys.path)"
RUN echo "Gunicorn location:" && which gunicorn || echo "Gunicorn not found in PATH"

# 7. USAR USUÁRIO NÃO-ROOT (segurança)
RUN useradd -m -u 1000 apiuser && chown -R apiuser:apiuser /app
USER apiuser

# 8. EXPOR PORTA
EXPOSE 5000

# 9. HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 10. COMANDO ALTERNATIVO - USANDO PYTHON DIRETAMENTE
# Opção A: Com gunicorn (recomendado para produção)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--worker-class", "sync", "--timeout", "120", "--access-logfile", "-", "fraud_detection_api:app"]

# Opção B: Com Flask diretamente (para desenvolvimento)
# CMD ["python", "fraud_detection_api.py"]