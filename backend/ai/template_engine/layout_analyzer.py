"""
Dynamic Layout Analyzer
"""


from reportlab.lib.pagesizes import A4





class LayoutAnalyzer:



    def analyze(

        self,

        template

    ):


        layout = template.get(

            "layout",

            {}

        )



        page="A4"



        if layout.get(

            "page_size"

        )=="A4":


            page_size=A4



        else:

            page_size=A4





        margins = layout.get(

            "margins",

            {}

        )



        return {



            "page_size":

            page_size,



            "margins":{


                "top":

                margins.get(
                    "top",
                    50
                ),



                "bottom":

                margins.get(
                    "bottom",
                    50
                ),



                "left":

                margins.get(
                    "left",
                    60
                ),



                "right":

                margins.get(
                    "right",
                    60
                )

            }

        }