class Tokenizer:

    @staticmethod
    def get_pair_words_from_list(word_list):
        try:
            pairs = set()
            for item in word_list:
                words = item.split()
                if len(words) > 1:
                    pairs.add(tuple(words))
            return pairs
        except Exception as e:
            raise Exception(f"Error while extracting pair words from list {e}")

    @staticmethod
    def tokenize(text: str):
        """Split on spaces, keep alphanumeric tokens only."""
        return [t.lower() for t in (text or "").split() if t.isalnum()]

    @staticmethod
    def lower_list_words(list):
        return [word.lower() for word in list]