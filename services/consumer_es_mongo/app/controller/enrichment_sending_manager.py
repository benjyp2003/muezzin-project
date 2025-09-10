import os
import threading

from services.consumer_es_mongo.app.es.es_processing import EsProcessor
from services.consumer_es_mongo.app.kafka.consumer import Consumer
from services.consumer_es_mongo.app.kafka.producer import Producer
from services.utils.logger import Logger


class EnrichmentTransactionManager:
    def __init__(self):
        self.producer = Producer().get_producer()
        self.consumer = Consumer()
        self.enrich_data_out_topic = os.environ.get("OUT_TOPIC", "pre_transcripts")
        self.enrich_data_in_topic = os.environ.get("IN_TOPIC", "transcripts")
        self.es_processor = EsProcessor()
        self.logger = Logger.get_logger()
        self.logger_lock = threading.Lock()



    def send(self, msg):
        try:
            self.logger.info(f"Sending msg for stt processing, to topic '{self.enrich_data_out_topic}'")
            self.producer.send(topic=self.enrich_data_out_topic, value=msg)
            self.logger.info(f"Sent msg - {msg} to topic '{self.enrich_data_out_topic}' successfully.\n")

        except Exception as e:
            raise Exception(f"Error sending msg to topic '{self.enrich_data_out_topic}' via kafka: {e}")

    def process_enrichment_data(self):
        try:
                self.logger.info(f"consuming messages from topic: '{self.enrich_data_out_topic}' ...\n")
                event = self.consumer.get_consumer_events(topic=self.enrich_data_in_topic, group="transcribed-group")
                for message in event:
                    msg = message.value
                    self.logger.info(f"\nReceived from topic - '{self.enrich_data_in_topic}'new data {msg}")
                    if msg:
                        text, id = msg.get("text"), msg.get("id")
                        self.es_processor.update_field_in_doc("text", text, id)
                        self.es_processor.update_field_in_doc("stt_status", "finished", id)

        except Exception as e:
            raise Exception(f"An error occurred while getting transcribed data: {e}")




