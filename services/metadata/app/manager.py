import os

from data_info import DataInfo
from pathlib import Path

from services.utils.logger import Logger
from services.metadata.app.kafka.kafka_producer import Producer


class Manager:
    def __init__(self, folder_path = r"C:\Users\benjy\PycharmProjects\muezzin-project\data\podcasts"):
        self.folder_path = folder_path
        self.producer = Producer().get_producer()
        self.topic = os.environ.get("TOPIC", "metadata")
        self.logger = Logger.get_logger()

    def process_metadata(self):
        try:
            pathlist = Path(self.folder_path).rglob('*.wav')
            self.logger.info(f"Running through all the .wav files in path '{self.folder_path}' and collecting metadata on each file...\n")
            for path in pathlist:
                data_info = DataInfo(path)
                info_dict = data_info.initialize_file_info_dict(str(path))
                self.logger.info(f"Initialized metadata dict successfully for file path - '{path}' \n")

                self.logger.info(f"Sending metadata dict to kafka topic - '{self.topic}' ...")
                self.producer.send(topic=self.topic,  value=info_dict)
                self.logger.info(f"Sent metadata to kafka successfully\n")

            self.logger.info("Flushing producer...")
            self.producer.flush()

        except Exception as e:
            self.logger.error(f"Error processing metadata: {e}")

if __name__ == "__main__":

    m = Manager()
    m.process_metadata()

