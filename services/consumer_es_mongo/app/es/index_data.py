import os

from services.consumer_es_mongo.app.es.es_client import EsClient
from services.consumer_es_mongo.app.es.mapping import MAPPING

class EsProcessor:
    def __init__(self):
        self.es = EsClient().get_client()
        self.index = os.environ.get("INDEX", "metadata-index")
        self.mapping = MAPPING

    def index_data(self, doc, id):
        try:
            self.ensure_index()
            print(f"Starting to index incoming doc on {self.index} index ...")
            self.es.index(index=self.index, id=id, body=doc)
            print("Indexed doc successfully")

        except Exception as e:
            raise Exception(f"Error during indexing: {e}")

    def ensure_index(self) -> None:
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, mappings=MAPPING)
        else:
            self.es.indices.delete(index=self.index)
            self.es.indices.create(index=self.index, mappings=MAPPING)

