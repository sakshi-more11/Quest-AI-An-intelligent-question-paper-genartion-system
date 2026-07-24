from backend.ai_engine.embeddings.embedding_generator import EmbeddingGenerator


class Retriever:

    def __init__(self, faiss_manager):

        self.faiss = faiss_manager
        self.embedder = EmbeddingGenerator()

    def search(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.embedder.generate_embedding(query)

        return self.faiss.search(
            query_embedding=query_embedding,
            top_k=top_k
        )