"""
semantic_search.py

Semantic search over the FAISS knowledge base.
"""

from backend.ai_engine.embeddings.embedding_generator import EmbeddingGenerator


class SemanticSearch:

    def __init__(self, faiss_manager):

        self.faiss = faiss_manager
        self.embedding_model = EmbeddingGenerator()

    def search(self, query, top_k=5):

        # Convert query into embedding
        query_embedding = self.embedding_model.generate_embedding(query)

        # Search FAISS
        results = self.faiss.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results