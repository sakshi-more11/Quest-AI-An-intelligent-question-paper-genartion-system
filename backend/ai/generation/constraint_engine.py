"""
QuestAI Constraint Satisfaction Engine

Selects the best set of questions
while satisfying generation constraints.
"""


class ConstraintEngine:


    def select_questions(
        self,
        questions,
        rules
    ):


        selected = []

        used_ids = set()

        current_marks = 0

        required_marks = rules["total_marks"]

        required_questions = rules["question_count"]


        covered_units = set()

        covered_cos = set()

        covered_bls = set()


        for q in questions:


            # -------------------------
            # Duplicate Check
            # -------------------------

            if q["id"] in used_ids:

                continue


            # -------------------------
            # Question Count
            # -------------------------

            if len(selected) >= required_questions:

                break


            # -------------------------
            # Marks Constraint
            # -------------------------

            if current_marks + q["marks"] > required_marks:

                continue


            # -------------------------
            # Select Question
            # -------------------------

            selected.append(q)

            used_ids.add(q["id"])

            current_marks += q["marks"]

            covered_units.add(q["unit"])

            covered_cos.add(q["co"])

            covered_bls.add(q["bl"])


        report = {

            "selected_questions": len(selected),

            "total_marks": current_marks,

            "covered_units": sorted(list(covered_units)),

            "covered_cos": sorted(list(covered_cos)),

            "covered_bls": sorted(list(covered_bls))

        }


        return selected, report