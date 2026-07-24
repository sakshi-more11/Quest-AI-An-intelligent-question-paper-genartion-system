"""
QuestAI Question Intelligence Engine

Step 11 - Block 3

Responsibilities
----------------
1. Generate SBERT Embeddings
2. Map Course Outcome (CO)
3. Detect Duplicate Questions
4. Store Intelligent Question
5. Bloom Taxonomy Classification
6. Difficulty Prediction
7. Question Enhancement
8. Vector Storage for RAG Retrieval
9. Generate AI Intelligence Report
"""


from backend.ai_engine.embeddings.sbert_engine import (
    SBERTEmbeddingEngine
)

from backend.ai_engine.co_mapping.co_mapper import (
    COMapper
)

from backend.ai_engine.question_bank.question_repository import (
    QuestionRepository
)

from backend.ai_engine.question_bank.question_schema import (
    QuestionSchema
)

from backend.ai_engine.retrieval.vector_store import (
    VectorStore
)

from backend.ai_engine.classifier.bloom_bert_classifier import (
    BloomBERTClassifier
)

from backend.ai_engine.classifier.difficulty_classifier import (
    DifficultyClassifier
)

from backend.ai_engine.enhancement.question_enhancer import (
    QuestionEnhancer
)



class QuestionIntelligence:


    def __init__(self):


        self.embedding_engine = SBERTEmbeddingEngine()

        self.co_mapper = COMapper()

        self.repository = QuestionRepository()

        self.vector_store = VectorStore()


        self.bloom_classifier = BloomBERTClassifier()

        self.difficulty_classifier = DifficultyClassifier()

        self.question_enhancer = QuestionEnhancer()



    # ==================================================
    # ANALYZE SINGLE QUESTION
    # ==================================================


    def analyze(self, question):


        text = question.get(
            "text",
            ""
        )


        print("\n==============================")
        print("AI INTELLIGENCE")
        print("==============================")


        print("Question:")
        print(text)



        # ---------------------------------------
        # QUESTION ENHANCEMENT
        # ---------------------------------------

        try:

            enhanced = self.question_enhancer.enhance(
                question
            )

            if enhanced:

                question = enhanced


        except Exception:

            pass



        text = question.get(
            "text",
            text
        )



        # ---------------------------------------
        # SBERT EMBEDDING
        # ---------------------------------------

        embedding = self.embedding_engine.generate_embedding(

            text

        )


        print(
            "Embedding Generated : YES"
        )



        # ---------------------------------------
        # BLOOM CLASSIFICATION
        # ---------------------------------------

        try:

            bloom_level = self.bloom_classifier.predict(

                text

            )

        except Exception:

            bloom_level = "BL1"



        print(
            "Bloom Level:",
            bloom_level
        )



        # ---------------------------------------
        # DIFFICULTY CLASSIFICATION
        # ---------------------------------------


        try:

            difficulty = self.difficulty_classifier.predict(

                text,

                question.get(
                    "marks",
                    0
                )

            )


        except Exception:

            difficulty = "Medium"



        print(
            "Difficulty:",
            difficulty
        )




        # ---------------------------------------
        # CO MAPPING
        # ---------------------------------------


        co_result = self.co_mapper.map_question(

            text

        )


        print(
            "Mapped CO:",
            co_result["co"]
        )


        print(
            "Confidence:",
            co_result["confidence"]
        )





        # ---------------------------------------
        # DUPLICATE CHECK
        # ---------------------------------------


        duplicate = self.repository.is_duplicate(

            text

        )


        print(
            "Duplicate:",
            duplicate
        )





        # ---------------------------------------
        # CREATE INTELLIGENT QUESTION
        # ---------------------------------------


        intelligent_question = QuestionSchema(


            text=text,


            marks=question.get(

                "marks",

                0

            ),


            unit=question.get(

                "unit",

                "Unknown"

            ),


            co=question.get(

                "co",

                co_result["co"]

            ),


            bl=bloom_level,


            difficulty=difficulty,


            embedding=embedding,


            confidence=co_result["confidence"]


        )






        # ---------------------------------------
        # STORE
        # ---------------------------------------


        if not duplicate:


            self.repository.add_question(

                intelligent_question

            )


            self.vector_store.add(

                embedding,

                intelligent_question.to_dict()

            )


            print(
                "Vector Stored : YES"
            )



        print(
            intelligent_question.to_dict()
        )



        return intelligent_question.to_dict()






    # ==================================================
    # ANALYZE MULTIPLE QUESTIONS
    # ==================================================


    def analyze_questions(self, questions):


        results=[]


        print(
            "\n==================================="
        )

        print(
            "QUESTION INTELLIGENCE REPORT"
        )

        print(
            "==================================="
        )



        for question in questions:


            results.append(

                self.analyze(question)

            )



        print(

            "\nRepository Size:",

            self.repository.count()

        )


        return results







    # ==================================================
    # RAG SEARCH
    # ==================================================


    def search(

        self,

        query

    ):


        embedding = self.embedding_engine.generate_embedding(

            query

        )


        return self.vector_store.search(

            embedding,

            5

        )






    # ==================================================
    # AI REPORT
    # ==================================================


    def report(self):


        try:

            vector_size = len(
                self.vector_store.vectors
            )

        except Exception:

            vector_size = 0



        return {


            "questions":

            self.repository.count(),



            "vector_store_size":

            vector_size,



            "ai_modules":

            [

                "SBERT Embedding",

                "CO Mapping",

                "Duplicate Detection",

                "RAG Vector Search",

                "BERT Bloom Classification",

                "Difficulty Classification",

                "Question Enhancement"

            ]

        }