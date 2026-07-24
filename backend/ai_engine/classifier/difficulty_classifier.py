"""
QuestAI Difficulty Classifier
"""


class DifficultyClassifier:


    def predict(
        self,
        text,
        marks
    ):


        text=text.lower()



        if marks <= 5:

            return "Easy"



        if marks <= 8:

            if any(
                word in text
                for word in [
                    "compare",
                    "analyze",
                    "derive"
                ]
            ):

                return "Medium"


            return "Medium"



        return "Hard"