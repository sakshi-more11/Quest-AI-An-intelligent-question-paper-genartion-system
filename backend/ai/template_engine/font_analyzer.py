"""
Font Analyzer

Detects font style information from OCR blocks.
"""


class FontAnalyzer:


    def analyze(self, extracted_data):

        fonts = []


        for page in extracted_data["pages"]:

            for block in page["blocks"]:

                text = block.get(
                    "text",
                    ""
                )


                if not text.strip():
                    continue


                bbox = block.get(
                    "bbox"
                )


                height = self.calculate_height(
                    bbox
                )


                fonts.append({

                    "text":text,

                    "size":height,

                    "bold":self.detect_bold(text)

                })


        return fonts



    def calculate_height(self,bbox):

        try:

            return abs(
                bbox[3][1]-bbox[0][1]
            )

        except:

            return 0



    def detect_bold(self,text):


        keywords=[

            "question",

            "course",

            "code",

            "name",

            "examination",

            "instructions"

        ]


        text=text.lower()


        return any(

            k in text

            for k in keywords

        )