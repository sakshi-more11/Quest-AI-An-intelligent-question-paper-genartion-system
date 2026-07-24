"""
QuestAI Template Aware Pagination Engine

Responsible for:
- automatic page breaks
- header/footer reservation
- repeated header
- repeated footer
- page numbering
"""


class PaginationEngine:


    def __init__(self):

        # A4 page points

        self.PAGE_HEIGHT = 842
        self.PAGE_WIDTH = 595


        # extracted from template

        self.TOP_MARGIN = 60
        self.BOTTOM_MARGIN = 50


        self.HEADER_HEIGHT = 100
        self.FOOTER_HEIGHT = 40



    def calculate_available_height(self):


        return (

            self.PAGE_HEIGHT

            -

            self.TOP_MARGIN

            -

            self.BOTTOM_MARGIN

            -

            self.HEADER_HEIGHT

            -

            self.FOOTER_HEIGHT

        )



    def paginate(

        self,

        questions,

        question_height=60

    ):


        pages=[]

        current_page=[]


        current_height=0



        available_height = (

            self.calculate_available_height()

        )



        for question in questions:


            if (

                current_height

                +

                question_height

                >

                available_height

            ):



                pages.append(

                    current_page

                )


                current_page=[]


                current_height=0



            current_page.append(

                question

            )


            current_height += question_height



        # remaining questions

        if current_page:


            pages.append(

                current_page

            )


        return pages





    def build_page_structure(

        self,

        pages

    ):


        result=[]


        total=len(pages)



        for index,page in enumerate(pages):


            result.append(


                {

                "page_number":index+1,


                "total_pages":total,


                "header":True,


                "footer":True,


                "questions":page


                }

            )


        return result