"""
QuestAI Template Schema

Step 10 - Block 3

Defines universal template structure
for all university question paper formats.

Supports:
- Header
- Logo
- Department
- Typography
- Layout
- Question styling
- CO/Bloom display
- Marks display
- Footer
- Signature
"""


DEFAULT_TEMPLATE_SCHEMA = {


    # =====================================
    # COLLEGE INFORMATION
    # =====================================

    "college": {

        "name": "",

        "logo": "",

        "department": ""

    },



    # =====================================
    # HEADER CONFIGURATION
    # =====================================

    "header": {


        "enabled": True,


        "available": True,


        "alignment": "center",


        "font": "Times-Bold",


        "size": 14,


        "exam_title":

            "End Semester Examination",



        "show_logo": True,


        "show_department": True,


        "show_college": True


    },



    # =====================================
    # TYPOGRAPHY
    # =====================================


    "typography": {


        "header": {


            "font": "Times-Bold",


            "size": 14,


            "alignment": "center"


        },


        "metadata": {


            "font": "Times-Roman",


            "size": 11,


            "alignment": "left"


        },


        "question": {


            "font": "Times-Roman",


            "size": 12,


            "leading": 16


        },


        "marks": {


            "font": "Times-Roman",


            "size": 11,


            "alignment": "right"


        }



    },



    # =====================================
    # PAGE LAYOUT
    # =====================================


    "layout": {


        "page_size": "A4",


        "margins": {


            "top": 50,


            "bottom": 50,


            "left": 60,


            "right": 60


        },


        "spacing": 1.5


    },



    # =====================================
    # QUESTION FORMAT
    # =====================================


    "question_format": {


        "numbering": "Q1",


        "style": "standard",


        "section_style": "SECTION A",


        "parts": [

            "A",

            "B"

        ],



        "marks_position": "right",



        "marks_format":

            "[{marks} Marks]",



        "show_co": True,


        "show_bloom": True,


        "show_difficulty": False



    },



    # =====================================
    # INSTRUCTIONS
    # =====================================


    "instructions": {


        "present": True,


        "title": "Instructions"



    },



    # =====================================
    # FOOTER
    # =====================================


    "footer": {


        "available": True,


        "signature": True,


        "signature_count": 2,


        "page_number": True,


        "text": ""

    },



    # =====================================
    # WATERMARK
    # =====================================


    "watermark": {


        "enabled": False,


        "text": ""

    }


}