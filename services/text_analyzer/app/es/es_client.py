from elasticsearch import Elasticsearch
import os


class EsClient:

    def __init__(self):
        self.host = os.getenv("ES_HOSTS", "http://localhost:9200")

        self.client = Elasticsearch(
            hosts=self.host,
            request_timeout=30
        )

    def get_client(self) -> Elasticsearch:
        """Return the raw Elasticsearch client if direct access is needed."""
        return self.client
