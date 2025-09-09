import os

import elasticsearch

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
            try:
                self.es.index(index=self.index, id=id, body=doc, op_type='create') # op_type='create' to ensure no duplicates
                self.logger.info("Indexed metadata successfully")
            except elasticsearch.exceptions.ConflictError:
                self.logger.warn(f"Document with ID '{id}' already exists. Skipping creation.")

        except Exception as e:
            raise Exception(f"Error during indexing: {e}")


    def ensure_index(self) -> None:
        try:
            if not self.es.indices.exists(index=self.index):
                self.es.indices.create(index=self.index, mappings=MAPPING)
                self.logger.info(f"Created index -{self.index}- successfully")
        except Exception as e:
            raise Exception(f"Error while creating index: {e}")


    def update_field_in_doc(self, field_name, value, id):
        try:
            self.es.update(
                index=self.index,
                id=id,
                body={"doc": {field_name: value}}
            )
            self.logger.info(f"Updated field '{field_name}' to es, with value '{value}', for id '{id}'")

        except Exception as e:
            self.logger.error("Error while adding new field to doc")
            raise Exception(f"Error while adding new field to doc: {e}")
