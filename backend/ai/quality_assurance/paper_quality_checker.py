"""
QuestAI Paper Quality Checker

Final validation before PDF export.

Step 9 - Batch 10

Validates:

- Header
- Footer
- Questions
- Marks
- CO
- BL
- Page count
- Structure
"""


class PaperQualityChecker:



    def __init__(self):

        pass




    # =================================================
    # MAIN VALIDATION
    # =================================================


    def validate(

        self,

        template,

        metadata,

        paper_structure,

        pages

    ):


        result = {


            "status":"PASSED",


            "checks":{},


            "errors":[]

        }




        # -------------------------
        # Header
        # -------------------------


        header = self.check_header(

            template

        )


        result["checks"]["header"] = header


        if not header:


            result["errors"].append(

                "Header missing"

            )




        # -------------------------
        # Footer
        # -------------------------


        footer = self.check_footer(

            template

        )


        result["checks"]["footer"] = footer


        if not footer:


            result["errors"].append(

                "Footer missing"

            )




        # -------------------------
        # Questions
        # -------------------------


        questions = self.check_questions(

            paper_structure

        )


        result["checks"]["questions"] = questions


        if not questions:


            result["errors"].append(

                "Questions missing"

            )




        # -------------------------
        # Marks
        # -------------------------


        marks = self.check_marks(

            paper_structure,

            metadata

        )


        result["checks"]["marks"] = marks


        if not marks:


            result["errors"].append(

                "Marks mismatch"

            )




        # -------------------------
        # CO BL
        # -------------------------


        co_bl = self.check_co_bl(

            paper_structure

        )


        result["checks"]["co_bl"] = co_bl


        if not co_bl:


            result["errors"].append(

                "CO/BL missing"

            )




        # -------------------------
        # Pages
        # -------------------------


        page_check = self.check_pages(

            pages

        )


        result["checks"]["pages"] = page_check


        if not page_check:


            result["errors"].append(

                "Invalid page count"

            )





        # Final Result


        if result["errors"]:


            result["status"]="FAILED"



        return result






    # =================================================
    # HEADER CHECK
    # =================================================


    def check_header(self,template):


        return (

            template.get(

                "header",

                {}

            ).get(

                "available",

                False

            )

        )





    # =================================================
    # FOOTER CHECK
    # =================================================


    def check_footer(self,template):


        return (

            template.get(

                "footer",

                {}

            ).get(

                "available",

                False

            )

        )






    # =================================================
    # QUESTION CHECK
    # =================================================


    def check_questions(self,paper_structure):


        if not paper_structure:

            return False



        count = 0



        for section in paper_structure:


            count += len(

                section.get(

                    "questions",

                    []

                )

            )



        return count > 0







    # =================================================
    # MARK CHECK
    # =================================================


    def check_marks(

        self,

        paper_structure,

        metadata

    ):


        total_marks = 0



        for section in paper_structure:


            for q in section.get(

                "questions",

                []

            ):


                for part in q.get(

                    "parts",

                    []

                ):


                    total_marks += part["question"].get(

                        "marks",

                        0

                    )



                # OR question marks

                if q.get("or"):


                    total_marks += q["or"]["question"].get(

                        "marks",

                        0

                    )




        expected = metadata.get(

            "total_marks",

            total_marks

        )



        return total_marks <= expected







    # =================================================
    # CO BL CHECK
    # =================================================


    def check_co_bl(

        self,

        paper_structure

    ):



        for section in paper_structure:


            for q in section.get(

                "questions",

                []

            ):



                for part in q.get(

                    "parts",

                    []

                ):



                    question = part["question"]



                    if (

                        not question.get("co")

                        or

                        not question.get("bl")

                    ):


                        return False





                # Check OR


                if q.get("or"):


                    question = q["or"]["question"]


                    if (

                        not question.get("co")

                        or

                        not question.get("bl")

                    ):

                        return False




        return True






    # =================================================
    # PAGE CHECK
    # =================================================


    def check_pages(self,pages):


        return pages > 0