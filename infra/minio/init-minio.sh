#!/bin/sh
set -e

echo "======================================"
echo " MinIO bootstrap — criando buckets"
echo "======================================"

echo "Aguardando MinIO ficar disponível..."

until mc alias set local http://minio:9000 minioadmin minioadmin; do
    echo "MinIO ainda não disponível, aguardando..."
    sleep 5
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
