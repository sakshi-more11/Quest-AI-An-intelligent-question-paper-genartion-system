from backend.ai.paper_generation.paper_schema import (

    PaperBlueprint,

    Section

)

from backend.ai.paper_generation.utils import (

    calculate_total_marks

)


class BlueprintGenerator:


    def generate(

        self,

        subject,

        exam_type,

        total_marks,

        units,

        bloom_distribution,

        difficulty_distribution

    ):

        if total_marks == 30:

            sections = [

                Section(

                    "Section A",

                    2,

                    5

                ),

                Section(

                    "Section B",

                    4,

                    5

                )

            ]


        elif total_marks == 50:

            sections = [

                Section(

                    "Section A",

                    2,

                    5

                ),

                Section(

                    "Section B",

                    4,

                    5

                ),

                Section(

                    "Section C",

                    10,

                    2

                )

            ]


        elif total_marks == 70:

            sections = [

                Section(

                    "Section A",

                    2,

                    5

                ),

                Section(

                    "Section B",

                    4,

                    5

                ),

                Section(

                    "Section C",

                    10,

                    4

                )

            ]


        else:

            raise Exception(

                "Unsupported paper format."

            )


        blueprint = PaperBlueprint(

            subject=subject,

            exam_type=exam_type,

            total_marks=calculate_total_marks(

                sections

            ),

            sections=sections,

            bloom_distribution=bloom_distribution,

            difficulty_distribution=difficulty_distribution,

            units=units

        )

        return blueprint