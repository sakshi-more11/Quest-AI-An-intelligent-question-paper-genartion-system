"""
Course Outcome Mapper

Assigns CO based on unit/topic
"""


class COMapper:



    def map(self,question):


        unit = question.get(

            "unit",

            ""

        )



        if "Unit 1" in unit:

            return "CO1"



        if "Unit 2" in unit:

            return "CO2"



        if "Unit 3" in unit:

            return "CO3"



        if "Unit 4" in unit:

            return "CO4"



        return "CO1"