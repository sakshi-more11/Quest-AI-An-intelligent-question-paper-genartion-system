from backend.ai_engine.retrieval.retriever import Retriever


class SearchService:

    def __init__(self, faiss_manager):

        self.retriever = Retriever(faiss_manager)

    def retrieve_context(
        self,
        query,
        top_k=5
    ):

        return self.retriever.search(
            query=query,
            top_k=top_k
        )