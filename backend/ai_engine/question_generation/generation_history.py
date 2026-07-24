"""
generation_history.py

Stores generated questions.
"""

class GenerationHistory:

    def __init__(self):

        self.history = []

    def add(self, question):

        self.history.append(question)

    def add_many(self, questions):

        self.history.extend(questions)

    def get_all(self):

        return self.history

    def clear(self):

        self.history.clear()