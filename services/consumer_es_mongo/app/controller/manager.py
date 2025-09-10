import os
import threading

from services.consumer_es_mongo.app.features.generate_id import generate_unique_id
from services.consumer_es_mongo.app.es.es_processing import EsProcessor
from services.consumer_es_mongo.app.mongo.dal import Dal

from services.consumer_es_mongo.app.controller.enrichment_sending_manager import EnrichmentTransactionManager
from services.consumer_es_mongo.app.kafka.consumer import Consumer
from services.consumer_es_mongo.app.kafka.producer import Producer
from services.utils.logger import Logger


class Manager:
    def __init__(self):
        self.consumer = Consumer()
        self.producer = Producer().get_producer()
        self.es_processor = EsProcessor()
        self.raw_data_topic = os.environ.get("TOPIC", "metadata")
        self.mongo_dal = Dal()
        self.stt_transaction_manager = EnrichmentTransactionManager()
        self.logger = Logger.get_logger()



    def consume_data(self):
            event = self.consumer.get_consumer_events(self.raw_data_topic, group="consumer_es_mongo-group")
            self.logger.info(f"Started consuming messages from topic: '{self.raw_data_topic}' ...")
            for message in event:
                msg = message.value
                if msg:
                     self.logger.info(f"\nReceived new data {msg}")

                     id = self.get_id(msg)

                     self.send_to_es_indexing(msg, id)
                     path = msg.get("path")
                     self.send_data_to_mongo(path, id)

                     stt_payload = {"path": path, "id": id}
                     self.send_data_for_stt(stt_payload)




    def get_id(self, msg):
        try:
            # Create a unique ID based on a hash of the file size and the file name
            size, file_name, path = msg["metadata"]["size_in_bytes"], msg["metadata"]["file_name"], msg.get("path")
            id = generate_unique_id(size, file_name)
            self.logger.info(f"Created unique id -{id}- for file: {msg["metadata"]["file_name"]}\n")
            return id
        except Exception as e:
            self.logger.error(f"Error generating unique id: {e}")

    def send_to_es_indexing(self, msg, id):
        try:
            msg.get("metadata")["stt_status"] = "pending"
            self.logger.info("Sending metadata for indexing...")
            self.es_processor.index_data(msg.get("metadata"), id)

        except Exception as e:
            self.logger.error(f"Error sending data to es indexing: {e}\n")

    def send_data_to_mongo(self, path, id):
        try:
            self.logger.info("\nSending path and id to mongo Dal...")
            self.mongo_dal.insert_audio_file(path, id)

        except Exception as e:
            self.logger.error(f"Error sending data to mongo: {e}\n")


    def send_data_for_stt(self, stt_payload):
        try:
            sending_thread = threading.Thread(target=self.stt_transaction_manager.send, args=[stt_payload], daemon=True)
            consuming_thread = threading.Thread(target=self.stt_transaction_manager.process_enrichment_data,
                                                daemon=True)
            sending_thread.start()
            consuming_thread.start()

        except Exception as e:
            self.logger.error(f"Error while threading the send and get from stt: {e}")


if __name__ == "__main__":
    m = Manager()
    m.consume_data()