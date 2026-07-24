"""
paper_optimizer.py

Main optimization pipeline for question paper generation.
"""


from backend.ai_engine.paper_optimizer.marks_allocator import MarksAllocator
from backend.ai_engine.paper_optimizer.question_selector import QuestionSelector
from backend.ai_engine.paper_optimizer.constraint_engine import ConstraintEngine



class PaperOptimizer:


    def __init__(self):

        self.marks_allocator = MarksAllocator()

        self.question_selector = QuestionSelector()

        self.constraint_engine = ConstraintEngine()



    def optimize(
        self,
        question_pool,
        total_marks
    ):


        # ---------------------------------
        # Step 1: Allocate Marks
        # ---------------------------------

        marks_distribution = self.marks_allocator.allocate(
            total_marks
        )


        # ---------------------------------
        # Step 2: Select Questions
        # ---------------------------------

        selected_questions = self.question_selector.select(
            question_pool,
            marks_distribution
        )


        # ---------------------------------
        # Step 3: Validate Paper
        # ---------------------------------

        validation = self.constraint_engine.validate(

            selected_questions,

            total_marks,

            total_marks

        )


        # ---------------------------------
        # Final Output
        # ---------------------------------

        return {


            "questions":
                selected_questions,


            "marks_distribution":
                marks_distribution,


            "validation":
                validation,


            "total_marks":
                total_marks

        }