import re

import spacy

from keybert import KeyBERT

from sentence_transformers import SentenceTransformer


class TopicExtractor:

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

        self.encoder = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.keybert = KeyBERT(
            self.encoder
        )

        self.stopwords = {
            "introduction",
            "definition",
            "chapter",
            "figure",
            "table",
            "example",
            "exercise",
            "summary",
            "references"
        }

    def clean(self, text):

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def split_sections(self, text):

        doc = self.nlp(text)

        sections = []

        current = ""

        for sent in doc.sents:

            current += " " + sent.text

            if len(current.split()) > 120:

                sections.append(current)

                current = ""

        if current:

            sections.append(current)

        return sections

    def extract_keywords(self, section):

        keywords = self.keybert.extract_keywords(

            section,

            keyphrase_ngram_range=(1,3),

            stop_words="english",

            top_n=8

        )

        result = []

        for word, score in keywords:

            word = word.strip()

            if len(word) < 3:

                continue

            if word.lower() in self.stopwords:

                continue

            result.append(word)

        return result

    def extract(self, text):

        text = self.clean(text)

        sections = self.split_sections(text)

        topics = []

        for section in sections:

            topics.extend(

                self.extract_keywords(section)

            )

        seen = set()

        final = []

        for topic in topics:

            t = topic.lower()

            if t not in seen:

                seen.add(t)

                final.append(topic)

        return final