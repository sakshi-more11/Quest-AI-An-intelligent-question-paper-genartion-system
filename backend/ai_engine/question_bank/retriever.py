class QuestionRetriever:

    def __init__(self, faiss_manager):
        self.faiss = faiss_manager

    def retrieve(self, top_k=20):

        chunks = self.faiss.get_all_chunks()

        print(
            "Retriever available chunks:",
            len(chunks)
        )

        return chunks[:top_k]