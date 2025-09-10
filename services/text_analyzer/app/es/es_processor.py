import os
from elasticsearch import Elasticsearch, helpers

from services.text_analyzer.app.features.analyzer import Analyzer
from services.text_analyzer.app.es.es_client import EsClient
from services.utils.logger import Logger


class EsProcessor:
    def __init__(self, analyzer: Analyzer):
        self.es = EsClient().get_client()
        self.index = os.environ.get("INDEX", "metadata-index")
        self.analyzer = analyzer
        self.logger = Logger.get_logger()


    def ensure_mapping(self, es: Elasticsearch):
        """Create or update index mapping with text_meta enrichment fields."""
        mapping = {
            "properties": {
                "text": {
                    "type": "text",
                },
                "text_metadata": {
                    "type": "object",
                    "properties": {
                        "bds_percent": {"type": "scaled_float", "scaling_factor": 1000},
                        "is_bds": {"type": "boolean"},
                        "bds_threat_level": {"type": "keyword"},
                    }
                }
            }
        }
        try:
            if not es.indices.exists(index=self.index):
                self.logger.info(f"Index '{self.index}' does not exist → creating it.")
                es.indices.create(index=self.index, mappings=mapping)
            else:
                self.logger.info(f"Index '{self.index}' exists → updating mapping.")
                es.indices.put_mapping(index=self.index, body=mapping)
        except Exception as e:
            raise Exception(f"Error ensuring mapping: {e}")

    def build_updates(self, es: Elasticsearch):
        """Yield update actions for bulk API."""
        try:
            scan = helpers.scan(
                es,
                index=self.index,
                query={"query": {"exists": {"field": "text"}}},
                _source_includes=["text"]
            )
            for hit in scan:
                yield {
                    "_op_type": "update",
                    "_index": self.index,
                    "_id": hit["_id"],
                    "doc": {"text_meta": self.analyzer.analyze(hit["_source"].get("text", ""))}
                }
        except Exception as e:
            raise Exception(f"Error during building updates: {e}")

    def update_text_metadata(self):

        # Ensure mapping is present
        self.ensure_mapping(self.es)

        # Bulk update
        self.logger.info("Updating documents with text metadata...")
        helpers.bulk(self.es, self.build_updates(self.es), chunk_size=500)
        self.logger.info("Successfully updated documents with text metadata.")


