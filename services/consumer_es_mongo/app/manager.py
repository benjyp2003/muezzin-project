import os
from pprint import pprint

from features.generate_id import generate_unique_id_with_timestamp
from es.index_data import EsProcessor
from mongo.dal import Dal
from services.consumer_es_mongo.app.kafka.consumer import Consumer

class Manager:
    def __init__(self):
        self.consumer = Consumer()
        self.es_processor = EsProcessor()
        self.topic = os.environ.get("TOPIC", "metadata")
        self.mongo_dal = Dal()


    def consume_data(self):
        try:
            event = self.consumer.get_consumer_events(self.topic)
            for msg in event:
                msg = msg.value
                create_date = msg["metadata"]["last_modified_date"]
                id = generate_unique_id_with_timestamp(create_date)
                pprint(msg.get("metadata"))
                self.es_processor.index_data(msg.get("metadata"), id)
                self.mongo_dal.insert_audio_file(msg.get("path"), id)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    m = Manager()
    m.consume_data()