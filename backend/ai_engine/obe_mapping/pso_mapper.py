"""
pso_mapper.py

Maps questions with Program Specific Outcomes.
"""


class PSOMapper:


    def __init__(self):


        # AI & ML department specific mapping

        self.mapping = {


            "CO1":
            [
                "PSO1"
            ],


            "CO2":
            [
                "PSO1",
                "PSO2"
            ],


            "CO3":
            [
                "PSO2",
                "PSO3"
            ]

        }



    def map_co(self, co):


        return self.mapping.get(
            co,
            []
        )



    def map_questions(self, questions):


        mapped_questions = []


        for q in questions:


            co = q.get(
                "CO"
            )


            q["PSO"] = self.map_co(
                co
            )


            mapped_questions.append(q)



        return mapped_questions