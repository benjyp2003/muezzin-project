import os

from services.text_analyzer.app.es.es_processor import EsProcessor
from services.text_analyzer.app.features.analyzer import Analyzer
from services.text_analyzer.app.features.decoder import base64_decoder
from services.utils.logger import Logger


class Manager:
    def __init__(self):
        self.dangerous_list = os.environ.get("THREATENING_WORDS", "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT")
        self.non_dangerous_list = os.environ.get("LESS_THREATENING_WORDS", "")
        self.analyzer = None
        self.logger = Logger().get_logger()


    def start_analyze(self):
        decoded_dangerous_list = base64_decoder(self.dangerous_list)
        self.logger.info(f"Decoded dangerous list successfully. list: {decoded_dangerous_list}")
        decoded_non_dangerous_list = base64_decoder(self.non_dangerous_list)
        self.logger.info(f"Decoded non-dangerous list successfully. list: {decoded_non_dangerous_list}\n")

        self.analyzer = Analyzer(decoded_dangerous_list, decoded_non_dangerous_list)
        es_processor = EsProcessor(self.analyzer)
        es_processor.update_text_metadata()

if __name__ == "__main__":
    manager = Manager()
    manager.start_analyze()