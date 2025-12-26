import json
from kafka import KafkaConsumer

def create_consumer(topic, group_id, bootstrap_servers):
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=True,
        auto_offset_reset="earliest"
    )
