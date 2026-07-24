"""
QuestAI Course Outcome Mapper

Responsibilities
----------------
1. Semantic CO Mapping
2. Similarity based matching
3. Confidence generation
"""

from backend.ai_engine.embeddings.sbert_engine import SBERTEmbeddingEngine


class COMapper:

    def __init__(self):

        self.embedding_engine = SBERTEmbeddingEngine()

        self.co_database = {

            "CO1": "Understand basic machine learning concepts, terminology and workflow.",

            "CO2": "Apply supervised learning algorithms for solving classification and regression problems.",

            "CO3": "Analyze advanced machine learning models and compare their performance.",

            "CO4": "Evaluate machine learning models using suitable performance metrics.",

            "CO5": "Design intelligent AI based solutions for real world applications."

        }

        self.co_embeddings = {}

        self.build_embeddings()

    # ==========================================
    # BUILD EMBEDDINGS
    # ==========================================

    def build_embeddings(self):

        for co, description in self.co_database.items():

            self.co_embeddings[co] = self.embedding_engine.generate_embedding(
                description
            )

    # ==========================================
    # MAP QUESTION
    # ==========================================

    def map_question(self, question):

        query_embedding = self.embedding_engine.generate_embedding(question)

        best_co = None
        best_score = -1

        for co, embedding in self.co_embeddings.items():

            score = self.embedding_engine.cosine_similarity(

                query_embedding,

                embedding

            )

            if score > best_score:

                best_score = score
                best_co = co

        return {

            "co": best_co,

            "confidence": round(best_score, 4)

        }

    # ==========================================
    # REPORT
    # ==========================================

    def report(self, question):

        result = self.map_question(question)

        return {

            "question": question,

            "mapped_co": result["co"],

            "confidence": result["confidence"]

        }