"""
QuestAI Header Renderer

Step 10 - Block 3

Responsible for:

- College name
- Department name
- Logo support
- Exam title
- Dynamic alignment
- University header format
"""


from reportlab.platypus import (
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib import colors

import os





class HeaderRenderer:



    def render(

        self,

        template,

        metadata,

        typography

    ):



        elements = []



        header = template.get(

            "header",

            {}

        )



        college = template.get(

            "college",

            {}

        )




        if not header.get(

            "enabled",

            True

        ):

            return elements






        # =====================================
        # LOGO + COLLEGE HEADER
        # =====================================


        logo_path = college.get(

            "logo",

            ""

        )



        college_name = metadata.get(

            "college_name",

            college.get(

                "name",

                ""

            )

        )



        department = college.get(

            "department",

            ""

        )



        exam_title = header.get(

            "exam_title",

            "End Semester Examination"

        )





        header_data = []





        left = ""

        right = []




        if (

            header.get("show_logo",True)

            and

            logo_path

            and

            os.path.exists(logo_path)

        ):



            logo = Image(

                logo_path,

                width=60,

                height=60

            )


            left = logo





        text = []




        if header.get(

            "show_college",

            True

        ):



            text.append(

                Paragraph(

                    f"<b>{college_name}</b>",

                    typography.header_style

                )

            )





        if header.get(

            "show_department",

            True

        ) and department:



            text.append(

                Paragraph(

                    department,

                    typography.header_style

                )

            )





        text.append(

            Paragraph(

                exam_title,

                typography.header_style

            )

        )




        header_data.append(

            [

                left,

                text

            ]

        )





        table = Table(

            header_data,

            colWidths=[80,350]

        )



        table.setStyle(

            TableStyle(

                [

                    (

                        "VALIGN",

                        (0,0),

                        (-1,-1),

                        "MIDDLE"

                    ),

                    (

                        "ALIGN",

                        (0,0),

                        (-1,-1),

                        "CENTER"

                    )

                ]

            )

        )





        elements.append(table)



        elements.append(

            Spacer(

                1,

                15

            )

        )



        return elements