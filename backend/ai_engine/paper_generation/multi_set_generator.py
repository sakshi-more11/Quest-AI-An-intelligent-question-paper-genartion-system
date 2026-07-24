"""
multi_set_generator.py

Generates multiple question paper sets.
"""


from backend.ai_engine.paper_optimizer.constraint_selector import ConstraintSelector
from backend.ai_engine.paper_generation.set_manager import SetManager



class MultiSetGenerator:



    def __init__(

        self,

        rules

    ):


        self.selector = ConstraintSelector(
            rules
        )


        self.manager = SetManager()



    def generate_sets(

        self,

        questions,

        number_of_sets,

        questions_per_set

    ):


        papers = []



        self.manager.reset()



        for set_number in range(

            1,

            number_of_sets + 1

        ):



            available_questions = []



            for q in questions:


                text = q["question"]



                if not self.manager.is_used(text):

                    available_questions.append(q)



            selected = self.selector.select(

                available_questions,

                questions_per_set

            )



            for q in selected:

                self.manager.add_question(
                    q["question"]
                )



            papers.append({

                "set_name":

                f"Set {chr(64+set_number)}",


                "questions":

                selected

            })



        return papers