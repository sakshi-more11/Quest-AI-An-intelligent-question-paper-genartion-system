"""
QuestAI Typography Manager

Step 10 - Block 3

Handles:

- Dynamic fonts
- Header typography
- Metadata typography
- Question typography
- Marks typography
- Alignment
- University template styling
"""


from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_RIGHT
)

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

import os





class TypographyManager:



    def __init__(

        self,

        typography_config=None

    ):



        self.config = typography_config or {}



        self.register_fonts()



        self.header_style = (

            self.create_header_style()

        )



        self.metadata_style = (

            self.create_metadata_style()

        )



        self.question_style = (

            self.create_question_style()

        )



        self.marks_style = (

            self.create_marks_style()

        )



        self.section_style = (

            self.create_section_style()

        )







    # =====================================================
    # FONT REGISTRATION
    # =====================================================


    def register_fonts(self):



        try:



            if os.path.exists(

                "Times New Roman.ttf"

            ):



                pdfmetrics.registerFont(

                    TTFont(

                        "Times-Roman",

                        "Times New Roman.ttf"

                    )

                )




            if os.path.exists(

                "Times New Roman Bold.ttf"

            ):



                pdfmetrics.registerFont(

                    TTFont(

                        "Times-Bold",

                        "Times New Roman Bold.ttf"

                    )

                )




        except Exception as e:


            print(

                "Font loading skipped:",

                e

            )







    # =====================================================
    # FONT NORMALIZER
    # =====================================================


    def normalize_font(

        self,

        font

    ):



        if not isinstance(

            font,

            str

        ):

            return "Times-Roman"





        font = font.lower()





        if "bold" in font:


            return "Times-Bold"





        return "Times-Roman"







    # =====================================================
    # HEADER STYLE
    # =====================================================


    def create_header_style(self):


        config = self.config.get(

            "header",

            {}

        )



        return ParagraphStyle(



            "HeaderStyle",



            fontName=self.normalize_font(

                config.get(

                    "font",

                    "Times-Bold"

                )

            ),



            fontSize=config.get(

                "size",

                14

            ),



            alignment=self.get_alignment(

                config.get(

                    "alignment",

                    "center"

                )

            ),



            leading=18



        )








    # =====================================================
    # SECTION STYLE
    # =====================================================


    def create_section_style(self):



        return ParagraphStyle(


            "SectionStyle",


            fontName="Times-Bold",


            fontSize=13,


            alignment=TA_LEFT,


            leading=16


        )







    # =====================================================
    # METADATA STYLE
    # =====================================================


    def create_metadata_style(self):


        config = self.config.get(

            "metadata",

            {}

        )



        return ParagraphStyle(



            "MetadataStyle",



            fontName=self.normalize_font(

                config.get(

                    "font",

                    "Times-Roman"

                )

            ),



            fontSize=config.get(

                "size",

                11

            ),



            alignment=self.get_alignment(

                config.get(

                    "alignment",

                    "left"

                )

            ),



            leading=15



        )







    # =====================================================
    # QUESTION STYLE
    # =====================================================


    def create_question_style(self):


        config = self.config.get(

            "question",

            {}

        )



        return ParagraphStyle(



            "QuestionStyle",



            fontName=self.normalize_font(

                config.get(

                    "font",

                    "Times-Roman"

                )

            ),



            fontSize=config.get(

                "size",

                12

            ),



            leading=config.get(

                "leading",

                16

            ),



            alignment=TA_LEFT



        )








    # =====================================================
    # MARK STYLE
    # =====================================================


    def create_marks_style(self):


        config = self.config.get(

            "marks",

            {}

        )



        return ParagraphStyle(



            "MarksStyle",



            fontName=self.normalize_font(

                config.get(

                    "font",

                    "Times-Roman"

                )

            ),



            fontSize=config.get(

                "size",

                11

            ),



            alignment=self.get_alignment(

                config.get(

                    "alignment",

                    "right"

                )

            )



        )







    # =====================================================
    # ALIGNMENT
    # =====================================================


    def get_alignment(

        self,

        value

    ):



        if value == "center":


            return TA_CENTER





        if value == "right":


            return TA_RIGHT





        return TA_LEFT