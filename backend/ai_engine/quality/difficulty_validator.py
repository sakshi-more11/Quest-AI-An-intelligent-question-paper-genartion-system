"""
QuestAI Difficulty Validator

Checks:
- Engineering level
- Question complexity
- Bloom level mapping
- Difficulty assignment
"""


class DifficultyValidator:



    def __init__(self):


        # Low level verbs

        self.basic_keywords = [

            "what is",

            "define",

            "list",

            "state",

            "name",

            "identify"

        ]



        # Engineering level verbs

        self.advanced_keywords = [

            "analyze",

            "design",

            "evaluate",

            "compare",

            "implement",

            "justify",

            "develop",

            "optimize",

            "architect",

            "investigate"

        ]




    # -----------------------------------
    # Validate Question
    # -----------------------------------

    def validate(

        self,

        question

    ):


        text = question.lower()



        score = 0



        # Basic keyword penalty

        for word in self.basic_keywords:


            if word in text:

                score -= 1



        # Advanced keyword reward

        for word in self.advanced_keywords:


            if word in text:

                score += 2



        # Length based complexity

        if len(text.split()) > 15:

            score += 1



        if len(text.split()) > 25:

            score += 1




        # Assign difficulty


        if score <= 0:


            difficulty = "Easy"



        elif score <= 2:


            difficulty = "Medium"



        else:


            difficulty = "Hard"



        return {


            "valid":

            score > 0,


            "difficulty":

            difficulty,


            "score":

            score

        }





    # -----------------------------------
    # Filter Questions
    # -----------------------------------

    def filter_questions(

        self,

        questions

    ):


        final_questions = []



        for q in questions:


            result = self.validate(

                q.get(

                    "question",

                    ""

                )

            )



            if result["valid"]:


                q["difficulty"] = result["difficulty"]


                final_questions.append(q)



        return final_questions