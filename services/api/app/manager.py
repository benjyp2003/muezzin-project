from services.api.app.es.es_processing import EsProcessor
from services.api.app.mongo.dal import Dal
from services.utils.logger import Logger


class Manager:
    def __init__(self):
        self.dal = Dal()
        self.es_processor = EsProcessor()
        self.logger = Logger.get_logger()

    def get_fields_values_from_es(self, field_name):
        try:
            return self.es_processor.get_all_field_values(field_name)
        except Exception as e:
            self.logger.error(f"Error retrieving field values from ES: {e}")
            return []

    def get_most_threatening_doc(self):
        try:
            return self.es_processor.get_most_threatening_text_doc()
        except Exception as e:
            self.logger.error(f"Error retrieving most threatening doc from MongoDB: {e}")
            return {}