"""
question_selector.py

Selects optimal questions for final paper.
"""


class QuestionSelector:


    def __init__(self):

        self.selected = []



    def select(
        self,
        question_pool,
        marks_distribution
    ):


        self.selected = []

        used_units = set()

        used_bloom = set()

        used_questions = set()



        for marks in marks_distribution:


            best_question = None


            for question in question_pool:


                text = question.get(
                    "question",
                    ""
                )


                # -------------------------
                # Skip duplicate
                # -------------------------

                if text in used_questions:

                    continue



                # -------------------------
                # Match marks
                # -------------------------

                if question.get(
                    "marks"
                ) != marks:

                    continue



                # -------------------------
                # Prefer new units
                # -------------------------

                score = 0


                if question.get(
                    "unit"
                ) not in used_units:

                    score += 2



                if question.get(
                    "bloom_level"
                ) not in used_bloom:

                    score += 2



                question["score"] = score



                if best_question is None:

                    best_question = question


                elif question["score"] > best_question["score"]:

                    best_question = question



            # Add selected question

            if best_question:


                self.selected.append(
                    best_question
                )


                used_questions.add(
                    best_question["question"]
                )


                used_units.add(
                    best_question.get("unit")
                )


                used_bloom.add(
                    best_question.get("bloom_level")
                )



        return self.selected