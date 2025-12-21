#!/bin/sh
set -e

echo "======================================"
echo " MinIO bootstrap — criando buckets"
echo "======================================"

echo "Aguardando MinIO ficar disponível..."

until mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"; do
    echo "MinIO ainda não disponível (alias)..."
    sleep 3
done

until mc ls local >/dev/null 2>&1; do
    echo "MinIO ainda não pronto para operações..."
    sleep 3
done

echo "MinIO disponível. Criando buckets..."

# --------------------------------------
# Data Lake (Arquitetura Medalhão)
# --------------------------------------
mc mb local/bronze --ignore-existing
mc mb local/silver --ignore-existing
mc mb local/gold --ignore-existing

# --------------------------------------
# Camadas adicionais
# --------------------------------------
mc mb local/ml-models --ignore-existing

echo "======================================"
echo " Buckets do MinIO criados com sucesso!"
echo "======================================"

echo "======================================"
echo " Populando modelos iniciais (Fraud Sentinel)"
echo "======================================"

# Caminho local dentro do container
SEED_DIR="/seed/fraud-sentinel/prod"

# Verificar se existem arquivos de seed
if [ -d "$SEED_DIR" ]; then
    echo "Copiando modelos iniciais para o bucket ml-models..."

    mc cp --recursive \
        "$SEED_DIR" \
        local/ml-models/fraud-sentinel/

    echo "Modelos iniciais copiados com sucesso!"
else
    echo "Diretório de seed não encontrado. Pulando carga inicial."
fi
