"""
retrieval_pipeline.py

Builds the complete retrieval pipeline.
"""

from backend.ai_engine.pipeline.preprocessing_pipeline import PreprocessingPipeline
from backend.ai_engine.knowledge_base.knowledge_builder import KnowledgeBuilder
from backend.ai_engine.vector_store.faiss_manager import FAISSManager
from backend.ai_engine.retrieval.search_service import SearchService


class RetrievalPipeline:

    def __init__(self):

        self.preprocessor = PreprocessingPipeline()
        self.builder = KnowledgeBuilder()
        self.faiss = FAISSManager()

    def build(self, file_path):

        # STEP 1
        processed_document = self.preprocessor.run(file_path)

        # STEP 2
        knowledge_records = self.builder.build(
            processed_document
        )

        # STEP 3
        self.faiss.build_index(
            knowledge_records
        )

        # Save index for later retrieval
        self.faiss.save("storage/knowledge_base")

        return SearchService(self.faiss)