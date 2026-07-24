"""
preprocessing_pipeline.py

Runs the complete preprocessing pipeline.
"""

from backend.ai_engine.preprocessing.document_processor import DocumentProcessor
from backend.ai_engine.classifier.document_classifier import DocumentClassifier
from backend.ai_engine.preprocessing.text_cleaner import TextCleaner
from backend.ai_engine.preprocessing.chunker import DocumentChunker
from backend.ai_engine.nlp.keyword_extractor import KeywordExtractor
from backend.ai_engine.nlp.topic_extractor import TopicExtractor


class PreprocessingPipeline:

    def __init__(self):

        self.processor = DocumentProcessor()

        self.classifier = DocumentClassifier()

        self.cleaner = TextCleaner()

        self.chunker = DocumentChunker()
        self.text_cleaner = TextCleaner()
        self.keyword_extractor = KeywordExtractor()

        self.topic_extractor = TopicExtractor()

    def run(self, file_path):

    # Step 1
        document = self.processor.process(file_path)

        # Step 2
        classification = self.classifier.classify(
            text=document["text"],
            filename=document["filename"],
            file_type=document["file_type"]
        )

        # Step 3
        cleaned_text = self.cleaner.clean(
            document["text"]
        )

        # Step 4
        chunks = self.chunker.chunk(cleaned_text)

        processed_chunks = []

        for index, chunk in enumerate(chunks):

            processed_chunks.append({

                "chunk_id": index + 1,

                "text": chunk,

                "keywords": self.keyword_extractor.extract(chunk),

                "topics": self.topic_extractor.extract(chunk)

            })

        return {

            "filename": document["filename"],

            "file_type": document["file_type"],

            "document_type": classification["document_type"],

            "confidence": classification["confidence"],

            "pages": document["pages"],

            "original_text": document["text"],

            "cleaned_text": cleaned_text,

            "chunks": processed_chunks

        }