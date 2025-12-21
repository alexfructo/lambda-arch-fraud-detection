#!/bin/sh
set -e

echo "======================================"
echo " Fraud Sentinel - Bootstrap de Modelos"
echo "======================================"

MINIO_ENDPOINT=${MINIO_ENDPOINT:-http://minio:9000}
MINIO_BUCKET=${MINIO_BUCKET:-ml-models}
MODEL_PREFIX=${MODEL_PREFIX:-fraud-sentinel/prod}
TARGET_DIR=/app/models

echo "Aguardando MinIO..."

until mc alias set local "$MINIO_ENDPOINT" "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"; do
  echo "MinIO ainda não disponível..."
  sleep 3
done

echo "MinIO disponível. Baixando modelos..."

mkdir -p "$TARGET_DIR"

RETRIES=5
COUNT=0

until mc cp --recursive "local/$MINIO_BUCKET/$MODEL_PREFIX" "$TARGET_DIR"; do
  COUNT=$((COUNT+1))
  if [ "$COUNT" -ge "$RETRIES" ]; then
    echo "Falha ao baixar modelos após $RETRIES tentativas"
    exit 1
  fi
  echo "Tentativa $COUNT/$RETRIES falhou. Retentando..."
  sleep 5
done

echo "Modelos baixados com sucesso"
echo "======================================"
