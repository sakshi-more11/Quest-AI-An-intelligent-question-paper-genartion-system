"""
QuestAI RAG Retriever

Retrieves semantically similar
questions from question bank
"""


class RAGRetriever:


    def __init__(
        self,
        vector_store,
        embedding_engine
    ):


        self.vector_store = vector_store

        self.embedding_engine = embedding_engine




    def retrieve(
        self,
        query,
        top_k=5
    ):


        embedding = self.embedding_engine.generate_embedding(
            query
        )


        return self.vector_store.search(

            embedding,

            top_k

        )