"""
constraint_engine.py

Validates question paper constraints.
"""


class ConstraintEngine:

    def __init__(self):

        self.errors = []
        self.warnings = []


    def validate(
        self,
        questions,
        total_marks,
        expected_marks
    ):

        self.errors = []
        self.warnings = []


        # -----------------------------
        # Check Total Marks
        # -----------------------------

        calculated_marks = sum(
            q.get("marks", 0)
            for q in questions
        )


        if calculated_marks != expected_marks:

            self.errors.append(
                f"Total marks mismatch. Expected {expected_marks}, Found {calculated_marks}"
            )


        # -----------------------------
        # Check Duplicate Questions
        # -----------------------------

        texts = []

        for q in questions:

            text = q.get(
                "question",
                ""
            ).lower()

            if text in texts:

                self.errors.append(
                    "Duplicate question detected"
                )

            texts.append(text)



        # -----------------------------
        # Check Marks Range
        # -----------------------------

        for q in questions:

            marks = q.get(
                "marks",
                0
            )

            if marks < 5:

                self.warnings.append(
                    "Question marks below recommended range"
                )


            if marks > 10:

                self.warnings.append(
                    "Question marks above recommended range"
                )


        # -----------------------------
        # Bloom Level Check
        # -----------------------------

        bloom_levels = set()

        for q in questions:

            if "bloom_level" in q:

                bloom_levels.add(
                    q["bloom_level"]
                )


        if len(bloom_levels) < 2:

            self.warnings.append(
                "Paper has limited Bloom Taxonomy coverage"
            )



        return {

            "valid":
                len(self.errors) == 0,

            "errors":
                self.errors,

            "warnings":
                self.warnings

        }