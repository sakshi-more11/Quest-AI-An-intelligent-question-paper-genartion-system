"""
set_manager.py

Manages multiple paper sets.
"""


class SetManager:


    def __init__(self):

        self.used_questions = set()



    def is_used(self, question):

        return question in self.used_questions



    def add_question(self, question):

        self.used_questions.add(
            question
        )



    def reset(self):

        self.used_questions.clear()