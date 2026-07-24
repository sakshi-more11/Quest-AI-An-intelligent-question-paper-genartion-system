"""
topic_extractor.py

Extract engineering topics using spaCy.
"""

import spacy

class TopicExtractor:

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text):

        doc = self.nlp(text)

        topics = []

        seen = set()

        # Extract noun chunks
        for chunk in doc.noun_chunks:

            topic = chunk.text.strip()

            if len(topic) > 3 and topic.lower() not in seen:

                topics.append(topic)

                seen.add(topic.lower())

        return topics