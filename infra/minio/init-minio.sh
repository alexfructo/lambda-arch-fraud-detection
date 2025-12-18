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
mc mb local/feature-store --ignore-existing
mc mb local/serving --ignore-existing

echo "======================================"
echo " Buckets do MinIO criados com sucesso!"
echo "======================================"