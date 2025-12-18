#!/bin/bash
set -e

: "${KAFKA_BOOTSTRAP_SERVERS:=kafka:29092}"

echo "======================================"
echo " Kafka bootstrap — criando tópicos"
echo "======================================"

echo "Aguardando Kafka ficar disponível (operação real)..."

until kafka-topics --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --list >/dev/null 2>&1; do
  echo "Kafka ainda não pronto para operações..."
  sleep 5
done

echo "Kafka disponível. Criando tópicos..."

kafka-topics \
  --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" \
  --create \
  --topic transactions_raw \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

echo "Tópico 'transactions_raw' OK"

kafka-topics \
  --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" \
  --create \
  --topic transactions_scored \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

echo "Tópico 'transactions_scored' OK"

echo "======================================"
echo " Kafka bootstrap finalizado com sucesso"
echo "======================================"
