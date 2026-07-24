"""
Difficulty Prediction Engine

Predicts:
Easy
Medium
Hard

Based on:
- question length
- keywords
- Bloom level
"""


class DifficultyEngine:


    def predict(self, question):


        text = question.get(
            "text",
            ""
        ).lower()



        score = 0



        # length based

        if len(text.split()) > 15:

            score += 1



        # advanced keywords

        keywords = [

            "derive",
            "compare",
            "analyze",
            "evaluate",
            "design",
            "architecture"

        ]


        for word in keywords:

            if word in text:

                score += 1




        if score >=3:

            return "Hard"



        elif score ==2:

            return "Medium"



        else:

            return "Easy"