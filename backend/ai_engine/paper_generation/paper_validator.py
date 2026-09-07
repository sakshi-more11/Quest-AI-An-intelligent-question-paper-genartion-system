"""
paper_validator.py

Validates generated question paper.
"""


class PaperValidator:


    def validate(self, paper):

        report = {

            "valid": True,

            "errors": [],

            "warnings": []

        }


        # -------------------------
        # Check Total Marks
        # -------------------------

        calculated_marks = 0


        questions = []


        for section in paper.get(
            "sections",
            []
        ):

            for q in section["questions"]:

                questions.append(q)

                calculated_marks += q.get(
                    "marks",
                    0
                )


        if calculated_marks != paper["total_marks"]:

            report["valid"] = False

            report["errors"].append(

                f"Marks mismatch. Expected {paper['total_marks']} Got {calculated_marks}"

            )


        # -------------------------
        # Duplicate Check
        # -------------------------

        texts = [

            q["question"]

            for q in questions

        ]


        if len(texts) != len(set(texts)):

            report["valid"] = False

            report["errors"].append(

                "Duplicate questions found"

            )


        # -------------------------
        # Empty Paper Check
        # -------------------------

        if len(questions)==0:

            report["valid"] = False

            report["errors"].append(

                "No questions generated"

            )

        bt1_count = sum(q.get("bloom_level", q.get("bloom")) == "BT1" for q in questions)
        if bt1_count > 1:
            report["valid"] = False
            report["errors"].append("A complete paper may contain at most one BT1 question")


        return report
