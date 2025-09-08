from kafka import KafkaConsumer
import json, os


class Consumer:
    def __init__(self):
        self.broker = os.getenv("BROKER", "localhost:9092")

    def get_consumer_events(self, topic):
        consumer = KafkaConsumer(topic,
                                 group_id="consumer_es_mongo-group",
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                 bootstrap_servers=self.broker,
                                 request_timeout_ms=30000,
                                 api_version=(2, 0, 2),
                                 auto_offset_reset='latest')

        return consumer
