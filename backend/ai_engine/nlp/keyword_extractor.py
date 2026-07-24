"""
keyword_extractor.py

Extract important keywords using KeyBERT.
"""

from keybert import KeyBERT


class KeywordExtractor:

    def __init__(self):

        self.model = KeyBERT(
            model="all-MiniLM-L6-v2"
        )

    def extract(
        self,
        text,
        top_n=10
    ):

        keywords = self.model.extract_keywords(

            text,

            keyphrase_ngram_range=(1, 3),

            stop_words="english",

            top_n=top_n

        )

        return [

            keyword

            for keyword, score in keywords

        ]