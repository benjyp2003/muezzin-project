import os
from elasticsearch import Elasticsearch

import elasticsearch
from elasticsearch_dsl import Search

from services.utils.logger import Logger
from services.consumer_es_mongo.app.es.es_client import EsClient
from services.consumer_es_mongo.app.es.mapping import MAPPING


class EsProcessor:
    def __init__(self):
        self.es = EsClient().get_client()
        self.index = os.environ.get("INDEX", "metadata-index")
        self.mapping = MAPPING
        self.logger = Logger.get_logger()


    def get_all_field_values(self, field_name):
        try:
            body = {
                "size": 0,  # Set size to 0 to only return aggregation results, not documents
                "aggs": {
                    "unique_field_values": {
                        "terms": {
                            "field": field_name,
                            "size": 10000
                        }
                    }
                }
            }
            # Execute the search request with the aggregation
            response = self.es.search(index=self.index, body=body)

            # Extract the values from the aggregation results
            field_values = []
            if 'aggregations' in response and 'unique_field_values' in response['aggregations']:
                for bucket in response['aggregations']['unique_field_values']['buckets']:
                    field_values.append(bucket['key'])

            return field_values
        except Exception as e:
            raise Exception(f"Error retrieving field values: {e}")


    def get_most_threatening_text_doc(self):
        try:
            s = Search(using=self.es, index=self.index)

            # 3. Sort the results by the desired field in descending order
            s = s.sort({
                "text_metadata.bds_percent": {"order": "desc"}
            })

            # 4. Limit the results to 1 to get only the document with the highest value
            s = s.extra(size=1)

            # 5. Execute the search
            response = s.execute()

            # 6. Process the results
            if response.hits:
                highest_value_doc = response.hits[0]
                self.logger.info(f"Document with highest value in 'your_field_name':")
                self.logger.info(f"ID: {highest_value_doc.meta.id}")
                self.logger.info(f"Source: {highest_value_doc.to_dict()}")
                return highest_value_doc.to_dict()
            else:
                self.logger.info("No documents found.")
                return {}
        except Exception as e:
            raise Exception(f"Error retrieving most threatening text doc: {e}")