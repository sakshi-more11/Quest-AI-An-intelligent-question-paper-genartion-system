"""
marks_allocator.py

Allocates marks distribution for question paper.
"""


class MarksAllocator:


    def __init__(self):

        self.allowed_marks = [
            5,
            10
        ]



    def allocate(
        self,
        total_marks,
        preferred_pattern=None
    ):


        distribution = []


        # ---------------------------------
        # If user provides pattern
        # ---------------------------------

        if preferred_pattern:

            return preferred_pattern



        # ---------------------------------
        # Automatic Allocation
        # ---------------------------------

        remaining = total_marks



        while remaining > 0:


            # Prefer 10 mark questions

            if remaining >= 10:

                distribution.append(10)

                remaining -= 10



            elif remaining >= 5:

                distribution.append(5)

                remaining -= 5



            else:

                break



        return distribution



    def count_questions(
        self,
        total_marks
    ):

        marks = self.allocate(
            total_marks
        )


        return {

            "total_marks":
                total_marks,

            "number_of_questions":
                len(marks),

            "distribution":
                marks

        }