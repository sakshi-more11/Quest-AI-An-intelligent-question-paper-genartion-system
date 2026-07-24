"""
QuestAI Vector Store

Stores SBERT embeddings
and performs similarity search
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



class VectorStore:


    def __init__(self):

        self.vectors = []

        self.documents = []



    def add(
        self,
        embedding,
        metadata
    ):

        self.vectors.append(
            embedding
        )

        self.documents.append(
            metadata
        )



    def search(
        self,
        query_embedding,
        top_k=5
    ):


        if not self.vectors:

            return []



        scores = cosine_similarity(

            [query_embedding],

            self.vectors

        )[0]



        indexes = np.argsort(
            scores
        )[::-1][:top_k]



        results=[]


        for index in indexes:

            item=self.documents[index].copy()

            item["similarity"] = float(
                scores[index]
            )

            results.append(item)



        return results