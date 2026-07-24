"""
QuestAI Generation Rules Engine

Creates and validates paper generation rules.

Batch 8:
- Section configuration
- Difficulty distribution
- Bloom distribution
- Question count
- Marks validation
"""


class RulesEngine:


    def __init__(self):

        pass



    # -------------------------------------------------

    def build_rules(self, config: dict):


        rules = {


            # -----------------------------
            # Paper Structure
            # -----------------------------

            "sections": config.get(

                "sections",

                [

                    {
                        "name": "SECTION A",
                        "questions": 2
                    },


                    {
                        "name": "SECTION B",
                        "questions": 2
                    },


                    {
                        "name": "SECTION C",
                        "questions": 2
                    }

                ]

            ),



            # -----------------------------
            # Question Generation Rules
            # -----------------------------


            "difficulty_distribution":

                config.get(

                    "difficulty_distribution",

                    {

                        "easy":30,

                        "medium":50,

                        "hard":20

                    }

                ),



            "bloom_distribution":

                config.get(

                    "bloom_distribution",

                    {

                        "BL1":20,

                        "BL2":20,

                        "BL3":30,

                        "BL4":20,

                        "BL5":10

                    }

                ),



            "question_count":

                config.get(

                    "question_count",

                    6

                ),



            "total_marks":

                config.get(

                    "total_marks",

                    100

                )

        }



        self.validate(rules)


        return rules




    # -------------------------------------------------

    def validate(self,rules):



        # Difficulty Check

        difficulty_total = sum(

            rules["difficulty_distribution"].values()

        )


        if difficulty_total != 100:


            raise Exception(

                "Difficulty distribution must equal 100%"

            )



        # Bloom Check

        bloom_total = sum(

            rules["bloom_distribution"].values()

        )


        if bloom_total != 100:


            raise Exception(

                "Bloom distribution must equal 100%"

            )



        # Question Count

        if rules["question_count"] <= 0:


            raise Exception(

                "Question count must be greater than zero"

            )



        # Marks

        if rules["total_marks"] <= 0:


            raise Exception(

                "Total marks must be greater than zero"

            )



        # Section Validation

        section_questions = sum(

            section["questions"]

            for section in rules["sections"]

        )


        if section_questions != rules["question_count"]:


            raise Exception(

                "Section question count does not match total question count"

            )



        return True