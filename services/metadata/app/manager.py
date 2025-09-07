import os

from data_info import DataInfo
from pathlib import Path

from services.metadata.app.kafka.kafka_producer import Producer

class Manager:
    def __init__(self, folder_path = r"C:\Users\benjy\PycharmProjects\muezzin-project\data\podcasts"):
        self.folder_path = folder_path
        self.producer = Producer().get_producer()
        self.topic = os.environ.get("TOPIC", "metadata")

    def process_metadata(self):
        try:
            pathlist = Path(self.folder_path).rglob('*.wav')
            for path in pathlist:
                data_info = DataInfo(path)
                info_dict = data_info.initialize_file_info_dict(str(path))
                print(f"sending info dict {info_dict} to kafka topic - {self.topic}...")
                self.producer.send(self.topic, info_dict)
                print("Data sent successfully")

        except Exception as e:
            print(f"An error accord: {e}")


if __name__ == "__main__":

    m = Manager()
    m.process_metadata()

