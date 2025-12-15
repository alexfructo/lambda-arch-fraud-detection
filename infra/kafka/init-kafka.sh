#!/bin/bash
set -e

echo "======================================"
echo " Kafka bootstrap — criando tópicos"
echo "======================================"

echo "Aguardando Kafka ficar disponível..."
cub kafka-ready -b kafka:29092 1 60

echo "Kafka disponível. Criando tópicos..."

# -------------------------------------------------
# Tópico: transações brutas (ingestão)
# -------------------------------------------------
kafka-topics \
  --bootstrap-server kafka:29092 \
  --create \
  --topic transactions_raw \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

echo "Tópico 'transactions_raw' OK"

# -------------------------------------------------
# (Opcional) Tópico: transações analisadas
# -------------------------------------------------
kafka-topics \
  --bootstrap-server kafka:29092 \
  --create \
  --topic transactions_scored \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

echo "Tópico 'transactions_scored' OK"

echo "======================================"
echo " Kafka bootstrap finalizado com sucesso"
echo "======================================"
