import os
from pymongo import MongoClient, errors
from gridfs import GridFS

from services.utils.logger import Logger


class Dal:
    def __init__(self):
        self.client = None
        self.db = None
        self.database_name = os.getenv("MONGO_DB_NAME", "podcasts")
        self.mongo_host = os.getenv("MONGO_HOST", "localhost")
        self.mongo_port = os.getenv("MONGO_PORT", "27017")
        self.uri = f"mongodb://{self.mongo_host}:{self.mongo_port}/"
        self.logger = Logger.get_logger()


    def insert_audio_file(self, file_path, id):
        """Insert a WAV file into MongoDB using GridFS."""
        try:
            with MongoClient(self.uri) as client:
                self.db = client[self.database_name]
                fs = GridFS(self.db)

                with open(file_path, 'rb') as file_data:
                    file_id = fs.put(file_data, id=id)
                self.logger.info(f"Inserted WAV file with unique id '{id}' into GridFS")
                self.logger.info("----------------------------------------------------\n")

        except Exception as e:
            raise Exception(f"Error inserting WAV file into GridFS: {e}")
