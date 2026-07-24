"""
QuestAI Professional PDF Template Renderer

Step 10 - Block 3 Complete

Features:

- Dynamic university template rendering
- Dynamic margins
- Dynamic typography
- Dynamic header
- Dynamic footer
- Logo support
- Section rendering
- Question numbering
- Marks formatting
- CO/Bloom visibility
- OR question rendering
- Instructions
- Multiple template compatibility
"""


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


from reportlab.lib import colors



from backend.ai.template_engine.typography_manager import (
    TypographyManager
)


from backend.ai.template_engine.layout_analyzer import (
    LayoutAnalyzer
)


from backend.ai.template_engine.header_renderer import (
    HeaderRenderer
)


from backend.ai.template_engine.footer_renderer import (
    FooterRenderer
)







class PDFTemplateRenderer:




    def __init__(self):


        self.layout_analyzer = LayoutAnalyzer()


        self.header_renderer = HeaderRenderer()


        self.footer_renderer = FooterRenderer()








    # =====================================================
    # MAIN RENDER FUNCTION
    # =====================================================


    def render(


        self,


        template,


        metadata,


        questions,


        output_path


    ):




        # -------------------------------------
        # Typography
        # -------------------------------------


        typography = TypographyManager(


            template.get(

                "typography",

                {}

            )

        )






        # -------------------------------------
        # Layout
        # -------------------------------------


        layout = self.layout_analyzer.analyze(

            template

        )



        margins = layout["margins"]






        document = SimpleDocTemplate(


            output_path,


            pagesize=layout["page_size"],


            leftMargin=margins["left"],


            rightMargin=margins["right"],


            topMargin=margins["top"],


            bottomMargin=margins["bottom"]


        )





        elements = []







        # =====================================================
        # HEADER
        # =====================================================


        elements.extend(


            self.header_renderer.render(

                template,

                metadata,

                typography

            )

        )







        # =====================================================
        # COURSE INFORMATION TABLE
        # =====================================================



        course_table = [


            [

                "Course Code",

                metadata.get(

                    "course_code",

                    ""

                )

            ],


            [

                "Course Name",

                metadata.get(

                    "course_name",

                    ""

                )

            ],



            [

                "Semester",

                metadata.get(

                    "semester",

                    ""

                )

            ],



            [

                "Maximum Marks",

                str(

                    metadata.get(

                        "total_marks",

                        ""

                    )

                )

            ]


        ]





        table = Table(

            course_table,

            colWidths=[130,320]

        )





        table.setStyle(


            TableStyle(

                [


                    (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                    ),



                    (

                    "VALIGN",

                    (0,0),

                    (-1,-1),

                    "MIDDLE"

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










        # =====================================================
        # INSTRUCTIONS
        # =====================================================



        instruction_config = template.get(

            "instructions",

            {}

        )





        if instruction_config.get(

            "present",

            False

        ):



            elements.append(


                Paragraph(

                    "<b>Instructions</b>",


                    typography.section_style

                )

            )



            for instruction in metadata.get(

                "instructions",

                []

            ):



                elements.append(


                    Paragraph(

                        str(instruction),

                        typography.question_style

                    )

                )



            elements.append(

                Spacer(

                    1,

                    15

                )

            )









        # =====================================================
        # QUESTION RENDERING
        # =====================================================



        show_co = template.get(

            "question_format",

            {}

        ).get(

            "show_co",

            True

        )



        show_bloom = template.get(

            "question_format",

            {}

        ).get(

            "show_bloom",

            True

        )





        marks_format = template.get(

            "question_format",

            {}

        ).get(

            "marks_format",

            "[{marks}]"

        )







        for section in questions:




            elements.append(


                Paragraph(


                    section.get(

                        "section_name",

                        "SECTION"

                    ),


                    typography.section_style

                )

            )





            elements.append(

                Spacer(

                    1,

                    10

                )

            )






            for q in section.get(

                "questions",

                []

            ):



                question_number = q.get(

                    "question_no",

                    ""

                )




                elements.append(


                    Paragraph(


                        f"<b>Q.{question_number}</b>",


                        typography.question_style

                    )

                )







                for part in q.get(

                    "parts",

                    []

                ):



                    question = part.get(

                        "question",

                        {}

                    )




                    marks = marks_format.format(

                        marks=question.get(

                            "marks",

                            ""

                        )

                    )






                    question_text = (


                        str(

                            part.get(

                                "label",

                                ""

                            )

                        )


                        + ") "


                        + str(

                            question.get(

                                "text",

                                ""

                            )

                        )


                        + " "


                        + marks


                    )






                    elements.append(


                        Paragraph(


                            question_text,


                            typography.question_style


                        )

                    )








                    metadata_line = ""



                    if show_co:



                        metadata_line += (

                            "CO: "

                            +

                            str(

                                question.get(

                                    "co",

                                    ""

                                )

                            )

                        )




                    if show_bloom:



                        metadata_line += (

                            "     BL: "

                            +

                            str(

                                question.get(

                                    "bl",

                                    ""

                                )

                            )

                        )





                    if metadata_line:



                        elements.append(


                            Paragraph(


                                metadata_line,


                                typography.metadata_style


                            )

                        )





                    elements.append(

                        Spacer(

                            1,

                            8

                        )

                    )








                # =====================================
                # OR QUESTION
                # =====================================



                if q.get(

                    "or"

                ):



                    elements.append(


                        Paragraph(


                            "<b>OR</b>",


                            typography.question_style


                        )

                    )





                    alternative = q["or"].get(

                        "question",

                        {}

                    )





                    elements.append(


                        Paragraph(


                            alternative.get(

                                "text",

                                ""

                            ),


                            typography.question_style


                        )

                    )






            elements.append(

                Spacer(

                    1,

                    15

                )

            )









        # =====================================================
        # FOOTER
        # =====================================================



        elements.extend(


            self.footer_renderer.render(

                template,

                typography

            )

        )








        # =====================================================
        # BUILD PDF
        # =====================================================



        document.build(

            elements

        )



        return output_path