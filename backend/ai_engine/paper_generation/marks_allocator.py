"""
marks_allocator.py

Handles question marks distribution.
"""


class MarksAllocator:


    def allocate(

        self,

        questions,

        required_marks

    ):

        allocated = []

        current_marks = 0


        for q in questions:


            if current_marks >= required_marks:

                break


            marks = q.get(
                "marks",
                0
            )


            if current_marks + marks <= required_marks:

                allocated.append(q)

                current_marks += marks


        return {

            "questions": allocated,

            "total_marks": current_marks,

            "remaining_marks": required_marks-current_marks

        }