"""
QuestAI Question Enhancement

Improves generated questions
"""


class QuestionEnhancer:



    def enhance(
        self,
        question
    ):


        enhanced = question.copy()



        text = question["text"]



        if not text.endswith("."):

            text += "."



        enhanced["text"] = text



        enhanced["quality"] = "Enhanced"



        return enhanced