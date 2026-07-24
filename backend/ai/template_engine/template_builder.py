"""
Template Builder

Converts analyzed question paper layout
into reusable QuestAI template JSON.

Batch 8:
Adds professional typography extraction.
"""


"""
Template Builder

Creates reusable QuestAI template JSON.
"""


class TemplateBuilder:


    def __init__(self):

        self.template_name="QuestAI_Template"



    def build(self,layout_data):


        return {


        "template_name":
        self.template_name,


        "college_name":
        self.extract_college_name(layout_data),



        "header":{


            "available":
            bool(
                layout_data.get(
                    "header"
                )
            ),


            "alignment":
            self.detect_alignment(
                layout_data.get(
                    "header",
                    []
                )
            ),


            "font":
            "Times-Bold",


            "size":
            14


        },



        "typography":{


            "header":{

                "font":
                "Times-Bold",

                "size":
                14,

                "alignment":
                "center"

            },


            "metadata":{


                "font":
                "Times-Roman",

                "size":
                12,

                "alignment":
                "left"

            },


            "question":{


                "font":
                "Times-Roman",

                "size":
                12,

                "leading":
                16

            },


            "marks":{


                "alignment":
                "right"

            }


        },



        "footer":{


            "available":
            True,


            "signature":
            self.detect_signature(
                layout_data.get(
                    "footer",
                    []
                )
            )

        },


        "page":{


            "margin":
            "1 inch"

        },



        "question_style":{


            "numbering":
            "Q.x",


            "marks_position":
            "right",


            "co_column":
            self.detect_keyword(
                layout_data,
                "CO"
            ),


            "bl_column":
            self.detect_keyword(
                layout_data,
                "BL"
            )


        },


        "instructions":{


            "present":
            bool(
                layout_data.get(
                    "instructions"
                )
            )

        }


        }



    def extract_college_name(self,data):


        for b in data.get("header",[]):

            text=b["text"]

            if "institute" in text.lower():

                return text


        return "Unknown"



    def detect_alignment(self,blocks):

        return "center"



    def detect_signature(self,footer):


        for b in footer:

            if "signature" in b["text"].lower():

                return True


        return False



    def detect_keyword(self,data,key):


        for section in data.values():

            if isinstance(section,list):

                for b in section:

                    if key.lower() in b["text"].lower():

                        return True


        return False