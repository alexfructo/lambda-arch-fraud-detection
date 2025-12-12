# init-scripts/init-kafka.sh

#!/bin/bash
echo "Esperando o Kafka ficar disponível..."
cub kafka-ready -b kafka:29092 1 60

echo "Criando o tópico 'transacoes'..."
kafka-topics --create \
  --topic transactions_raw \
  --bootstrap-server kafka:29092 \
  --partitions 1 \
  --replication-factor 1 \
  --if-not-exists

echo "Tópico do Kafka criado com sucesso!"
