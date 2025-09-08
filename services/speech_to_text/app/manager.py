import os

from services.speech_to_text.app.kafka.consumer import Consumer
from services.speech_to_text.app.kafka.producer import Producer
from services.speech_to_text.app.model.transcriber import Transcriber
from services.utils.logger import Logger


class Manager:
    def __init__(self):
        self.in_topic = os.getenv("IN_TOPIC", "metadata")
        self.out_topic = os.getenv("OUT_TOPIC", "transcripts")
        self.consumer = Consumer()
        self.producer = Producer().get_producer()
        self.transcriber =Transcriber()
        self.logger = Logger.get_logger()

    def execute_speech_to_text(self):
        try:
            event = self.consumer.get_consumer_events(self.in_topic)
            self.logger.info(f"Started consuming messages from topic: '{self.in_topic}' ...\n")

            for msg in event:
                msg = msg.value
                if msg:
                    self.logger.info(f"\nReceived new data {msg}")

                    path = msg.get("path")
                    self.logger.info(f"Starting stt on file from path {path}")
                    text = self.transcriber.transcribe_file(path)
                    if text:
                        self.logger.info(f"Transcribed audio to text successfully, text: {text}")
                    else:
                        self.logger.warn("Text came back empty from transcribing")

                    self.logger.info("Adding 'text' field to the msg...")
                    msg["text"] = text

                    self.logger.info(f"Sending msg - {msg} to kafka topic - '{self.out_topic}'")
                    self.producer.send(topic=self.out_topic, value=msg)
                    self.logger.info(f"Message sent to kafka topic - '{self.out_topic}' successfully.")

        except Exception as e:
            self.logger.error(e)

if __name__ == "__main__":
    m = Manager()
    m.execute_speech_to_text()