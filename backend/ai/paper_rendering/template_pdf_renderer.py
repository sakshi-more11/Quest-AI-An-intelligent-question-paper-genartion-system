"""
Professional Template PDF Renderer

Uses:
- Coordinate Renderer
- Style Manager
- Spacing Engine
- Template Mapper

This renderer is responsible for generating
professional university-style question papers.
"""

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

# -------- NEW IMPORTS --------

from backend.ai.renderer.coordinate_renderer import CoordinateRenderer
from backend.ai.renderer.style_manager import StyleManager
from backend.ai.renderer.spacing_engine import SpacingEngine
from backend.ai.renderer.template_mapper import TemplateMapper



class TemplatePDFRenderer:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.coordinate_renderer = CoordinateRenderer()

        self.style_manager = StyleManager()

        self.spacing = SpacingEngine()

        self.mapper = TemplateMapper()

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------

    def build_header(
        self,
        elements,
        metadata,
        template
    ):

        header_style = self.styles["Heading2"]

        header_style.alignment = TA_CENTER

        style = self.style_manager.get_header_style()

        header_style.fontName = style["font"]

        header_style.fontSize = style["size"]

        elements.append(

            Paragraph(

                metadata.get(
                    "college_name",
                    "College Name"
                ),

                header_style

            )

        )

        elements.append(

            Spacer(
                1,
                self.spacing.HEADER_GAP
            )

        )

        title_style = self.styles["Heading3"]

        title_style.alignment = TA_CENTER

        title = metadata.get(
            "exam_name",
            "End Semester Examination"
        )

        elements.append(

            Paragraph(
                title,
                title_style
            )

        )

        elements.append(

            Spacer(
                1,
                self.spacing.TITLE_GAP
            )

        )

    # -------------------------------------------------
    # METADATA
    # -------------------------------------------------

    def build_metadata(
        self,
        elements,
        metadata
    ):

        data = [

            [
                "Course Code",
                metadata.get(
                    "course_code",
                    ""
                ),

                "Date",
                metadata.get(
                    "date",
                    ""
                )
            ],

            [
                "Course Name",
                metadata.get(
                    "course_name",
                    ""
                ),

                "Time",
                metadata.get(
                    "time",
                    ""
                )
            ],

            [
                "Class",
                metadata.get(
                    "class",
                    ""
                ),

                "Max Marks",
                str(

                    metadata.get(
                        "max_marks",
                        ""
                    )

                )

            ]

        ]

        table = Table(

            data,

            colWidths=[
                90,
                180,
                80,
                120
            ]

        )

        table.setStyle(

            TableStyle(

                [

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.black
                    ),

                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.lightgrey
                    ),

                    (
                        "BACKGROUND",
                        (2, 0),
                        (2, -1),
                        colors.lightgrey
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, -1),
                        "Times-Roman"
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        10
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    )

                ]

            )

        )

        elements.append(table)

        elements.append(

            Spacer(

                1,

                self.spacing.SECTION_GAP

            )

        )
            # -------------------------------------------------
    # INSTRUCTIONS
    # -------------------------------------------------

    def build_instructions(
        self,
        elements,
        metadata
    ):

        title = Paragraph(

            "<b>Instructions :</b>",

            self.styles["Heading4"]

        )

        elements.append(title)

        instructions = metadata.get(

            "instructions",

            [

                "1. All questions are compulsory.",

                "2. Figures in right column indicate marks.",

                "3. Assume suitable data wherever necessary.",

                "4. Use of non-programmable calculator is allowed."

            ]

        )

        for ins in instructions:

            elements.append(

                Paragraph(

                    ins,

                    self.styles["Normal"]

                )

            )

        elements.append(

            Spacer(

                1,

                self.spacing.SECTION_GAP

            )

        )



    # -------------------------------------------------
    # QUESTION RENDERER
    # -------------------------------------------------

    def build_questions(

        self,

        elements,

        questions

    ):

        current_question = None

        current_sub = None

        for q in questions:

            question_number = str(

                q.get(

                    "number",

                    ""

                )

            )

            sub_part = q.get(

                "sub",

                "A"

            )

            marks = str(

                q.get(

                    "marks",

                    ""

                )

            )

            co = q.get(

                "co",

                ""

            )

            bl = q.get(

                "bl",

                ""

            )

            text = q.get(

                "text",

                ""

            )

            if question_number != current_question:

                current_question = question_number

                elements.append(

                    Spacer(

                        1,

                        self.spacing.QUESTION_GAP

                    )

                )

                elements.append(

                    Paragraph(

                        f"<b>Q.{question_number}</b>",

                        self.styles["Heading3"]

                    )

                )

            if sub_part != current_sub:

                current_sub = sub_part

                elements.append(

                    Spacer(

                        1,

                        8

                    )

                )



            row = [

                [

                    Paragraph(

                        f"<b>{sub_part})</b>",

                        self.styles["Normal"]

                    ),

                    Paragraph(

                        text,

                        self.styles["Normal"]

                    ),

                    Paragraph(

                        f"<b>{marks}</b>",

                        self.styles["Normal"]

                    ),

                    Paragraph(

                        co,

                        self.styles["Normal"]

                    ),

                    Paragraph(

                        bl,

                        self.styles["Normal"]

                    )

                ]

            ]



            table = Table(

                row,

                colWidths=[

                    28,

                    315,

                    45,

                    45,

                    45

                ]

            )



            table.setStyle(

                TableStyle(

                    [

                        (

                            "VALIGN",

                            (0,0),

                            (-1,-1),

                            "TOP"

                        ),

                        (

                            "BOTTOMPADDING",

                            (0,0),

                            (-1,-1),

                            8

                        ),

                        (

                            "ALIGN",

                            (2,0),

                            (-1,-1),

                            "CENTER"

                        ),

                        (

                            "FONTNAME",

                            (0,0),

                            (-1,-1),

                            "Times-Roman"

                        ),

                        (

                            "FONTSIZE",

                            (0,0),

                            (-1,-1),

                            11

                        )

                    ]

                )

            )

            elements.append(

                table

            )



    # -------------------------------------------------
    # OR BLOCK
    # -------------------------------------------------

    def add_or_block(

        self,

        elements

    ):

        elements.append(

            Spacer(

                1,

                6

            )

        )

        elements.append(

            Paragraph(

                "<b><center>OR</center></b>",

                self.styles["Heading4"]

            )

        )

        elements.append(

            Spacer(

                1,

                6

            )

        )
        # -------------------------------------------------
    # PAGE HEADER
    # -------------------------------------------------

    def draw_page_header(self, canvas, document):

        canvas.saveState()

        width, height = A4

        canvas.setFont("Times-Bold", 14)

        canvas.drawCentredString(
            width / 2,
            height - 40,
            document.college_name
        )

        canvas.setFont("Times-Bold", 12)

        canvas.drawCentredString(
            width / 2,
            height - 58,
            document.exam_name
        )

        canvas.line(
            40,
            height - 68,
            width - 40,
            height - 68
        )

        canvas.restoreState()



    # -------------------------------------------------
    # PAGE FOOTER
    # -------------------------------------------------

    def draw_page_footer(self, canvas, document):

        canvas.saveState()

        width, _ = A4

        canvas.line(
            40,
            55,
            width - 40,
            55
        )

        canvas.setFont(
            "Times-Roman",
            10
        )

        canvas.drawString(
            45,
            35,
            "Exam Centre : _____________"
        )

        canvas.drawRightString(
            width - 45,
            35,
            f"Page {canvas.getPageNumber()}"
        )

        canvas.restoreState()



    # -------------------------------------------------
    # PAGE CALLBACK
    # -------------------------------------------------

    def on_page(
        self,
        canvas,
        document
    ):

        self.draw_page_header(
            canvas,
            document
        )

        self.draw_page_footer(
            canvas,
            document
        )



    # -------------------------------------------------
    # SIGNATURE BLOCK
    # -------------------------------------------------

    def build_signature(
        self,
        elements
    ):

        elements.append(
            Spacer(
                1,
                30
            )
        )

        table = Table(

            [

                [

                    "Examiner Signature",

                    "",

                    "HOD Signature"

                ]

            ],

            colWidths=[
                170,
                120,
                170
            ]

        )

        table.setStyle(

            TableStyle(

                [

                    (
                        "LINEABOVE",
                        (0,0),
                        (0,0),
                        0.5,
                        colors.black
                    ),

                    (
                        "LINEABOVE",
                        (2,0),
                        (2,0),
                        0.5,
                        colors.black
                    ),

                    (
                        "ALIGN",
                        (0,0),
                        (-1,-1),
                        "CENTER"
                    ),

                    (
                        "TOPPADDING",
                        (0,0),
                        (-1,-1),
                        15
                    ),

                    (
                        "FONTNAME",
                        (0,0),
                        (-1,-1),
                        "Times-Roman"
                    )

                ]

            )

        )

        elements.append(table)



    # -------------------------------------------------
    # PAGE BREAK
    # -------------------------------------------------

    def add_page_break_if_needed(
        self,
        elements,
        estimated_lines
    ):

        from reportlab.platypus import PageBreak

        if estimated_lines > 28:

            elements.append(
                PageBreak()
            )



    # -------------------------------------------------
    # LONG QUESTION SPACING
    # -------------------------------------------------

    def estimate_lines(
        self,
        text
    ):

        words = len(
            text.split()
        )

        return max(
            1,
            words // 12
        )

        # -------------------------------------------------
    # MAIN RENDER FUNCTION
    # -------------------------------------------------

    def render(
        self,
        template,
        metadata,
        questions,
        output_path
    ):

        document = SimpleDocTemplate(

            output_path,

            pagesize=A4,

            rightMargin=40,
            leftMargin=40,
            topMargin=80,
            bottomMargin=60

        )

        # Needed for page callbacks
        document.college_name = metadata.get(
            "college_name",
            "College Name"
        )

        document.exam_name = metadata.get(
            "exam_name",
            "End Semester Examination"
        )

        elements = []

        # ---------------------------------------
        # HEADER
        # ---------------------------------------

        self.build_header(

            elements,

            metadata,

            template

        )

        # ---------------------------------------
        # COURSE DETAILS
        # ---------------------------------------

        self.build_metadata(

            elements,

            metadata

        )

        # ---------------------------------------
        # INSTRUCTIONS
        # ---------------------------------------

        self.build_instructions(

            elements,

            metadata

        )

        # ---------------------------------------
        # QUESTIONS
        # ---------------------------------------

        current_question = None

        for question in questions:

            # automatic page spacing

            lines = self.estimate_lines(

                question.get(
                    "text",
                    ""
                )

            )

            self.add_page_break_if_needed(

                elements,

                lines

            )

            # OR block

            if question.get(
                "or",
                False
            ):

                self.add_or_block(

                    elements

                )

            # Render one question

            self.build_questions(

                elements,

                [

                    question

                ]

            )

        # ---------------------------------------
        # SIGNATURE
        # ---------------------------------------

        self.build_signature(

            elements

        )

        # ---------------------------------------
        # BUILD PDF
        # ---------------------------------------

        document.build(

            elements,

            onFirstPage=self.on_page,

            onLaterPages=self.on_page

        )

        return output_path    