"""
Intelligent Question Selection Engine
"""


from backend.ai.question_selection.difficulty_engine import (
    DifficultyEngine
)

from backend.ai.question_selection.bloom_mapper import (
    BloomMapper
)

from backend.ai.question_selection.co_mapper import (
    COMapper
)

from backend.ai.question_selection.similarity_checker import (
    SimilarityChecker
)

from backend.ai.question_selection.constraint_solver import (
    ConstraintSolver
)





class QuestionSelector:



    def __init__(self):


        self.difficulty = DifficultyEngine()

        self.bloom = BloomMapper()

        self.co = COMapper()

        self.similarity = SimilarityChecker()

        self.constraint = ConstraintSolver()





    def select(

        self,

        question_bank,

        count,

        total_marks


    ):



        selected=[]



        for q in question_bank:



            q["difficulty"]=self.difficulty.predict(q)


            q["bl"]=self.bloom.map(q)


            q["co"]=self.co.map(q)




            duplicate=self.similarity.check_duplicate(

                selected+[q]

            )



            if duplicate:

                continue



            selected.append(q)



            if len(selected)==count:

                break





        validation=self.constraint.validate(

            selected,

            total_marks

        )




        return {


            "questions":selected,


            "validation":validation


        }