#!/bin/sh

# Espera o MinIO ficar disponível
until mc alias set myminio http://minio:9000 minioadmin minioadmin; do
    echo "Esperando pelo MinIO..."
    sleep 5
done

# Cria os buckets da arquitetura Lambda
mc mb myminio/bronze --ignore-existing
mc mb myminio/silver --ignore-existing
mc mb myminio/gold --ignore-existing
mc mb myminio/feature_store --ignore-existing
mc mb myminio/serving --ignore-existing

echo "Buckets do MinIO criados com sucesso!"
