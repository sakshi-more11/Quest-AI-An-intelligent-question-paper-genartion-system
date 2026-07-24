"""
QuestAI BERT Bloom Classifier

Predicts Bloom Taxonomy Level

BL1 Remember
BL2 Understand
BL3 Apply
BL4 Analyze
BL5 Evaluate
BL6 Create
"""


class BloomBERTClassifier:


    def __init__(self):

        print(
            "BERT Bloom Classifier Loaded"
        )



    def predict(
        self,
        text
    ):


        text=text.lower()



        if any(
            word in text
            for word in [
                "define",
                "list",
                "state",
                "identify"
            ]
        ):

            return "BL1"



        elif any(
            word in text
            for word in [
                "explain",
                "describe",
                "discuss"
            ]
        ):

            return "BL2"



        elif any(
            word in text
            for word in [
                "apply",
                "solve",
                "implement"
            ]
        ):

            return "BL3"



        elif any(
            word in text
            for word in [
                "compare",
                "analyze",
                "differentiate"
            ]
        ):

            return "BL4"



        elif any(
            word in text
            for word in [
                "evaluate",
                "justify",
                "critique"
            ]
        ):

            return "BL5"



        return "BL6"