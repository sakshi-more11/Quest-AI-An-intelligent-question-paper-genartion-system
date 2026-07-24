"""
QuestAI Bloom Taxonomy Mapper

Automatically maps questions
to Bloom's Taxonomy levels.

BT1 - Remember
BT2 - Understand
BT3 - Apply
BT4 - Analyze
BT5 - Evaluate
BT6 - Create
"""


class BloomMapper:



    def __init__(self):


        self.mapping = {



            "BT1": [

                "define",

                "list",

                "state",

                "identify",

                "name",

                "describe"

            ],




            "BT2": [

                "explain",

                "summarize",

                "discuss",

                "interpret",

                "illustrate"

            ],




            "BT3": [

                "apply",

                "use",

                "implement",

                "solve",

                "demonstrate"

            ],




            "BT4": [

                "analyze",

                "compare",

                "differentiate",

                "examine",

                "investigate"

            ],




            "BT5": [

                "evaluate",

                "justify",

                "critique",

                "assess",

                "review"

            ],




            "BT6": [

                "design",

                "develop",

                "create",

                "propose",

                "construct"

            ]

        }




    # -----------------------------------
    # Map Single Question
    # -----------------------------------

    def classify(

        self,

        question

    ):


        text = question.lower()



        scores = {

            level:0

            for level in self.mapping

        }





        for level, keywords in self.mapping.items():


            for keyword in keywords:


                if keyword in text:


                    scores[level] += 1






        # Highest matching level

        bloom_level = max(

            scores,

            key=scores.get

        )




        # If no keyword found

        if scores[bloom_level] == 0:


            bloom_level = "BT4"






        return bloom_level






    # -----------------------------------
    # Apply to Question List
    # -----------------------------------

    def map_questions(

        self,

        questions

    ):



        for question in questions:



            question_text = question.get(

                "question",

                ""

            )



            question["blooms_level"] = self.classify(

                question_text

            )



        return questions