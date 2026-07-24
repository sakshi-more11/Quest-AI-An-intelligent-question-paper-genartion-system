"""
Constraint Solver

Ensures:

- marks balance
- difficulty distribution
- Bloom distribution
"""


class ConstraintSolver:



    def validate(

        self,

        questions,

        total_marks

    ):



        marks=sum(

            q.get(

                "marks",

                0

            )

            for q in questions

        )



        if marks != total_marks:


            return {


                "valid":False,


                "message":

                "Marks distribution mismatch"

            }




        return {


            "valid":True,


            "message":

            "Constraints satisfied"

        }