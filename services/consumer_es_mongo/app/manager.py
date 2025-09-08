import os

from features.generate_id import generate_unique_id
from es.index_data import EsProcessor
from mongo.dal import Dal
from services.consumer_es_mongo.app.kafka.consumer import Consumer
from services.utils.logger import Logger


class Manager:
    def __init__(self):
        self.consumer = Consumer()
        self.es_processor = EsProcessor()
        self.topic = os.environ.get("TOPIC", "transcripts")
        self.mongo_dal = Dal()
        self.logger = Logger.get_logger()


    def consume_data(self):
        try:
            event = self.consumer.get_consumer_events(self.topic)
            self.logger.info(f"Started consuming messages from topic: '{self.topic}' ...\n")
            for msg in event:
                msg = msg.value
                if msg:
                    self.logger.info(f"Received new data {msg}")
                    # Create a unique ID based on the file size in bytes and a random number
                    size = msg["metadata"]["size_in_bytes"]
                    id = generate_unique_id(size)
                    self.logger.info(f"Created unique id -{id}- for file: {msg["metadata"]["file_name"]}\n")

                    self.logger.info("Sending metadata for indexing...")
                    self.es_processor.index_data(msg.get("metadata"), id)

                    self.logger.info("\nSending path and id to mongo Dal...")
                    self.mongo_dal.insert_audio_file(msg.get("path"), id)

        except Exception as e:
            self.logger.error(e)

if __name__ == "__main__":
    m = Manager()
    m.consume_data()