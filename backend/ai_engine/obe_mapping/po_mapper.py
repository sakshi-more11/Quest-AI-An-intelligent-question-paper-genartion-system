"""
po_mapper.py

Maps Course Outcomes to Program Outcomes.
"""


class POMapper:


    def __init__(self):

        # CO to PO relationship
        # Based on common NBA OBE mapping

        self.mapping = {


            "CO1":
            [
                "PO1",
                "PO2"
            ],


            "CO2":
            [
                "PO3",
                "PO5"
            ],


            "CO3":
            [
                "PO2",
                "PO3",
                "PO12"
            ]

        }



    def map_co(self, co):


        return self.mapping.get(
            co,
            []
        )



    def map_questions(self, questions):


        mapped_questions=[]


        for q in questions:


            co = q.get(
                "CO"
            )


            q["PO"] = self.map_co(
                co
            )


            mapped_questions.append(q)



        return mapped_questions