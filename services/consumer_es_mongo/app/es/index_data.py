import os

from services.utils.logger import Logger
from services.consumer_es_mongo.app.es.es_client import EsClient
from services.consumer_es_mongo.app.es.mapping import MAPPING


class EsProcessor:
    def __init__(self):
        self.es = EsClient().get_client()
        self.index = os.environ.get("INDEX", "metadata-index")
        self.mapping = MAPPING
        self.logger = Logger.get_logger()

    def index_data(self, doc, id):
        try:
            self.ensure_index()
            self.logger.info(f"Starting to index incoming metadata with id - '{id}', on '{self.index}' index ...")
            self.es.index(index=self.index, id=id, body=doc)
            self.logger.info("Indexed metadata successfully")

        except Exception as e:
            raise Exception(f"Error during indexing: {e}")

    def ensure_index(self) -> None:
        try:
            if not self.es.indices.exists(index=self.index):
                self.es.indices.create(index=self.index, mappings=MAPPING)
                self.logger.info(f"Created index -{self.index}- successfully")


        except Exception as e:
            raise Exception(f"Error while creating index: {e}")
