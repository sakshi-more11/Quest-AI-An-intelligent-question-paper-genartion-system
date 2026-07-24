"""
QuestAI Intelligent Question Repository

Stores intelligent questions with embeddings.
"""

from backend.ai_engine.embeddings.sbert_engine import SBERTEmbeddingEngine

from backend.ai_engine.question_bank.question_schema import (
    QuestionSchema
)


class QuestionRepository:

    def __init__(self):

        self.embedding_engine = SBERTEmbeddingEngine()

        self.questions = []

    # =====================================
    # ADD QUESTION
    # =====================================

    def add_question(

        self,

        question: QuestionSchema

    ):

        if question.embedding is None:

            question.embedding = self.embedding_engine.generate_embedding(

                question.text

            )

        self.questions.append(question)

    # =====================================
    # ADD MULTIPLE
    # =====================================

    def add_questions(

        self,

        questions

    ):

        for question in questions:

            self.add_question(question)

    # =====================================
    # GET ALL
    # =====================================

    def get_all(self):

        return [

            question.to_dict()

            for question in self.questions

        ]

    # =====================================
    # SEARCH
    # =====================================

    def semantic_search(

        self,

        query

    ):

        if len(self.questions) == 0:

            return None

        question_bank = [

            question.to_dict()

            for question in self.questions

        ]

        return self.embedding_engine.most_similar(

            query,

            question_bank

        )

    # =====================================
    # DUPLICATE CHECK
    # =====================================

    def is_duplicate(

        self,

        text

    ):

        for question in self.questions:

            if self.embedding_engine.is_duplicate(

                text,

                question.text

            ):

                return True

        return False

    # =====================================
    # SIZE
    # =====================================

    def count(self):

        return len(self.questions)