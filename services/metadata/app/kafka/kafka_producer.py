import json, os
from kafka import KafkaProducer


class Producer:
    def __init__(self):
        self.broker = os.getenv("BROKER", "localhost:9092")

    def get_producer(self):
        producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
        )
        return producer