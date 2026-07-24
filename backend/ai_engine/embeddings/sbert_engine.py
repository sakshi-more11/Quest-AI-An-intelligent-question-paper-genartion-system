"""
QuestAI SBERT Embedding Engine

Responsibilities
----------------
1. Load MiniLM only once
2. Generate embeddings
3. Compute cosine similarity
4. Duplicate detection support
5. Semantic search support
"""


import numpy as np

from sentence_transformers import SentenceTransformer


class SBERTEmbeddingEngine:


    _model = None


    def __init__(self):

        if SBERTEmbeddingEngine._model is None:

            print("\n==============================")
            print("LOADING SBERT MODEL")
            print("==============================")

            SBERTEmbeddingEngine._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

            print("MiniLM Loaded Successfully\n")

        self.model = SBERTEmbeddingEngine._model


    # ============================================
    # SINGLE EMBEDDING
    # ============================================

    def generate_embedding(self, text):

        if not isinstance(text, str):

            text = str(text)

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding.tolist()


    # ============================================
    # MULTIPLE EMBEDDINGS
    # ============================================

    def generate_embeddings(self, texts):

        texts = [str(t) for t in texts]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings.tolist()


    # ============================================
    # COSINE SIMILARITY
    # ============================================

    def cosine_similarity(

        self,

        embedding1,

        embedding2

    ):

        e1 = np.array(embedding1)

        e2 = np.array(embedding2)

        similarity = np.dot(e1, e2)

        return float(similarity)


    # ============================================
    # DUPLICATE CHECK
    # ============================================

    def is_duplicate(

        self,

        text1,

        text2,

        threshold=0.90

    ):

        emb1 = self.generate_embedding(text1)

        emb2 = self.generate_embedding(text2)

        similarity = self.cosine_similarity(

            emb1,

            emb2

        )

        return similarity >= threshold


    # ============================================
    # MOST SIMILAR QUESTION
    # ============================================

    def most_similar(

        self,

        query,

        question_bank

    ):

        query_embedding = self.generate_embedding(query)

        best_score = -1

        best_question = None

        for question in question_bank:

            score = self.cosine_similarity(

                query_embedding,

                question["embedding"]

            )

            if score > best_score:

                best_score = score

                best_question = question

        return {

            "question": best_question,

            "similarity": round(best_score, 4)

        }


    # ============================================
    # EMBEDDING REPORT
    # ============================================

    def report(

        self,

        text

    ):

        embedding = self.generate_embedding(text)

        return {

            "text": text,

            "dimension": len(embedding),

            "generated": True

        }