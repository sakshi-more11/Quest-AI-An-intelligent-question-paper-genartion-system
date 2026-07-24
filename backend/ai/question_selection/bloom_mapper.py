"""
Bloom Taxonomy Mapper

Maps questions to:

BL1 Remember
BL2 Understand
BL3 Apply
BL4 Analyze
BL5 Evaluate
BL6 Create
"""


class BloomMapper:



    def map(self, question):


        text = question.get(

            "text",

            ""

        ).lower()



        mapping={


            "define":"BL1",

            "list":"BL1",

            "explain":"BL2",

            "describe":"BL2",

            "apply":"BL3",

            "implement":"BL3",

            "analyze":"BL4",

            "compare":"BL4",

            "evaluate":"BL5",

            "design":"BL6"

        }



        for key,value in mapping.items():


            if key in text:

                return value



        return "BL2"