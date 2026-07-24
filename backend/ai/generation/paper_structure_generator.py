"""
QuestAI Paper Structure Generator

Creates professional
Section-based Question Paper.
"""


class PaperStructureGenerator:

    def generate(

        self,

        structured_questions,

        rules

    ):

        sections = rules.get(

            "sections",

            [

                {

                    "name": "SECTION A",

                    "questions": 2

                },

                {

                    "name": "SECTION B",

                    "questions": 2

                }

            ]

        )

        paper = []

        current = 0

        for section in sections:

            sec = {

                "section_name": section["name"],

                "questions": []

            }

            count = section["questions"]

            while (

                count > 0

                and

                current < len(structured_questions)

            ):

                sec["questions"].append(

                    structured_questions[current]

                )

                current += 1

                count -= 1

            paper.append(sec)

        return paper