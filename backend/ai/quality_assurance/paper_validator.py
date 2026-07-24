"""
QuestAI Final Paper Quality Assurance Engine

Phase 8 Step 8
Batch 10 Complete
"""


class PaperValidator:



    def validate(
        self,
        template,
        metadata,
        questions,
        pdf_info=None,
        coordinates=None
    ):


        report = {


            "status": True,


            "errors": [],


            "warnings": [],


            "checks": {}

        }



        checks = report["checks"]



        # Header

        checks["header"] = self.check_header(
            template
        )


        # Footer

        checks["footer"] = self.check_footer(
            template
        )


        # Metadata

        checks["metadata"] = self.check_metadata(
            metadata
        )


        # Questions

        checks["questions"] = self.check_questions(
            questions
        )


        # Marks

        checks["marks"] = self.check_marks(
            questions
        )


        # CO

        checks["co_mapping"] = self.check_co(
            questions
        )


        # Bloom

        checks["bloom_level"] = self.check_bl(
            questions
        )


        # Question numbering

        checks["question_sequence"] = (
            self.check_question_sequence(
                questions
            )
        )


        # Layout

        checks["layout"] = (
            self.check_layout(
                coordinates
            )
        )



        # Page

        checks["pagination"] = (
            self.check_pages(
                pdf_info
            )
        )




        for name,value in checks.items():


            if value is False:


                report["errors"].append(
                    name+" validation failed"
                )



        if report["errors"]:


            report["status"]=False



        return report





    # -----------------------------
    # HEADER
    # -----------------------------


    def check_header(self,template):


        return (
            template
            .get("header",{})
            .get("available",False)
        )





    # -----------------------------
    # FOOTER
    # -----------------------------


    def check_footer(self,template):


        return (
            template
            .get("footer",{})
            .get("available",False)
        )





    # -----------------------------
    # METADATA
    # -----------------------------


    def check_metadata(self,metadata):


        required=[

            "college_name",
            "course_code",
            "course_name"

        ]


        return all(
            metadata.get(x)
            for x in required
        )





    # -----------------------------
    # QUESTIONS
    # -----------------------------


    def check_questions(self,questions):


        if not questions:

            return False


        for q in questions:


            if "number" not in q:

                return False



        return True





    # -----------------------------
    # MARKS
    # -----------------------------


    def check_marks(self,questions):


        for q in questions:


            if q.get("number") in [
                "Q.1",
                "Q.2",
                "Q.3",
                "Q.4",
                "Q.5",
                "Q.6"
            ]:

                continue



            if "marks" not in q:


                return False



        return True





    # -----------------------------
    # CO
    # -----------------------------


    def check_co(self,questions):


        for q in questions:


            if q.get("number")=="Q.1":

                continue



            if not q.get("co"):


                return False



        return True





    # -----------------------------
    # BLOOM LEVEL
    # -----------------------------


    def check_bl(self,questions):


        allowed=[

            "BL1",
            "BL2",
            "BL3",
            "BL4",
            "BL5",
            "BL6"

        ]


        for q in questions:


            if q.get("number")=="Q.1":

                continue



            if q.get("bl") not in allowed:


                return False



        return True





    # -----------------------------
    # QUESTION NUMBERING
    # -----------------------------


    def check_question_sequence(
        self,
        questions
    ):


        numbers=[]


        for q in questions:


            if q["number"].startswith("Q"):


                numbers.append(
                    q["number"]
                )



        if not numbers:

            return False



        return True





    # -----------------------------
    # PAGE CHECK
    # -----------------------------


    def check_pages(self,pdf_info):


        if pdf_info is None:

            return True



        pages = pdf_info.get(
            "pages",
            0
        )


        if pages <=0:

            return False



        return True





    # -----------------------------
    # COORDINATE OVERLAP
    # -----------------------------


    def check_layout(self,coordinates):


        if coordinates is None:

            return True



        blocks = coordinates



        for i in range(
            len(blocks)
        ):


            for j in range(
                i+1,
                len(blocks)
            ):


                if self.overlap(
                    blocks[i],
                    blocks[j]
                ):


                    return False



        return True




    def overlap(self,a,b):


        ax1=a["x"]
        ay1=a["y"]

        ax2=ax1+a["width"]
        ay2=ay1+a["height"]



        bx1=b["x"]
        by1=b["y"]

        bx2=bx1+b["width"]
        by2=by1+b["height"]



        return (

            ax1 < bx2
            and
            ax2 > bx1
            and
            ay1 < by2
            and
            ay2 > by1

        )