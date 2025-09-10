import os

from services.text_analyzer.app.features.tokenizer import Tokenizer
from services.utils.logger import Logger


class Analyzer:
    def __init__(self, dangerous_list, less_dangerous_list):
        self.tokenizer = Tokenizer()
        self.dangerous_list = self.tokenizer.lower_list_words(dangerous_list)
        self.less_dangerous_list = self.tokenizer.lower_list_words(less_dangerous_list)
        self.threshold = os.environ.get("THRESHOLD", 15)
        self.logger = Logger.get_logger()


    def analyze(self, text: str) -> dict:
        """ Analyze the text and return the results """
        tokens = self.tokenizer.tokenize(text)
        total = len(tokens)

        # Extract the word paris out of the lists
        threatening_pairs = self.tokenizer.get_pair_words_from_list(self.dangerous_list)
        non_threatening_pairs = self.tokenizer.get_pair_words_from_list(self.less_dangerous_list)

        # Find the matching words
        word_hits, pair_hits = self.get_hits(tokens, threatening_pairs, non_threatening_pairs)
        hit_count, non_threatening_count = self.count_hits(word_hits, pair_hits, non_threatening_pairs)

        # Calc the percentage of threat words / total words
        percentage = self.get_danger_percentage(hit_count, non_threatening_count, total)

        return dict(
            bds_percent=percentage,
            is_bds=self.classify_text_if_criminalized(percentage),
            bds_threat_level=self.get_text_level_of_danger(hit_count, percentage)
        )

    def get_hits(self, tokens, threatening_pairs, non_threatening_pairs):
        try:

            # word matches
            word_hits = [t for t in tokens if t in self.dangerous_list or t in self.less_dangerous_list]
            # pair matches
            pair_hits = [
                f"{a} {b}"
                for a, b in zip(tokens, tokens[1:])
                if (a, b) in threatening_pairs or (a, b) in non_threatening_pairs
            ]
            return word_hits, pair_hits

        except Exception as e:
            raise Exception(f"Error finding matching words in text: {e}")

    def count_hits(self, word_hits, pair_hits, non_threatening_pairs):
        # Count the amount of non threatening words found
        non_threatening_count = len([1 for word in word_hits if word in self.less_dangerous_list])
        non_threatening_paris_count = len([1 for word in pair_hits if tuple(word.split()) in non_threatening_pairs])
        non_threatening_count += non_threatening_paris_count

        return len(word_hits) + len(pair_hits), non_threatening_count

    @staticmethod
    def get_danger_percentage(hit_count, non_threatening_count, total):
        try:
            # Calculate the danger % according to the hit count - exclude half from the non threatening words count, mult by 100 to get the percentage and dev by total
            return ((hit_count - (non_threatening_count * 0.5)) * 100.0) / total
        except Exception as e:
            raise Exception(f"Error calculating danger percent: {e}")

    def classify_text_if_criminalized(self, percent):
        if percent > self.threshold:
            return True
        else:
            return False

    @staticmethod
    def get_text_level_of_danger(hit_count, percent):
        if percent < 10:
            if hit_count > 1000:
                return "high"
            elif hit_count >= 100:
                return "medium"
            elif hit_count >= 10:
                return "low"
            else:
                return "none"
        elif percent < 20:
            return "medium"
        else:
            return "high"


