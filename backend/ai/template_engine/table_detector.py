"""
Question Table Detector

Detects:
Marks column
CO column
Bloom Level column
"""


class TableDetector:


    def detect(self, layout, extracted_data=None):


        result = {

            "marks_column": False,

            "co_column": False,

            "bl_column": False,

            "question_numbering":"unknown"

        }


        text = ""


        # Existing layout data

        for section in layout.values():

            for block in section:

                text += (
                    block.get("text","")
                    .lower()
                    +" "
                )


        # Raw OCR backup

        if extracted_data:


            for page in extracted_data["pages"]:

                for block in page["blocks"]:

                    text += (

                        block.get("text","")
                        .lower()
                        +" "

                    )



        print("\nTABLE DETECTOR TEXT")

        print(text[:1000])



        # Marks

        marks_words=[

            "marks",

            "(08)",

            "(04)",

            "(06)",

            "(10)"

        ]


        if any(
            word in text
            for word in marks_words
        ):

            result["marks_column"]=True



        # CO

        if (
            "co" in text
            or "course outcome" in text
        ):

            result["co_column"]=True



        # Bloom

        if (

            "bl" in text

            or

            "bt" in text

            or

            "bloom" in text

        ):

            result["bl_column"]=True



        # Question numbering


        if "q.1" in text:

            result["question_numbering"]="Q.x"


        elif "1." in text:

            result["question_numbering"]="number"



        return result