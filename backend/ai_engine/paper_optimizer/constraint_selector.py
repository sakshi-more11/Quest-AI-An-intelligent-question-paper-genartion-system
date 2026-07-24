"""
constraint_selector.py

Advanced Constraint Based Question Selector.
"""


class ConstraintSelector:


    def __init__(self, rules):

        self.rules = rules



    def select(

        self,

        questions,

        total_questions

    ):


        selected = []


        difficulty_count = {}

        bloom_count = {}

        unit_count = {}



        for question in questions:



            if len(selected) >= total_questions:

                break



            if self._check_constraint(

                question,

                difficulty_count,

                bloom_count,

                unit_count,

                total_questions

            ):



                selected.append(question)



                self._update_count(

                    question,

                    difficulty_count,

                    bloom_count,

                    unit_count

                )



        return selected





    def _check_constraint(

        self,

        question,

        difficulty_count,

        bloom_count,

        unit_count,

        total_questions

    ):



        difficulty = question.get(
            "difficulty"
        )


        bloom = question.get(
            "bloom_level"
        )


        unit = question.get(
            "unit"
        )



        # -----------------------------
        # Difficulty Check
        # -----------------------------


        max_allowed = (

            self.rules["difficulty_distribution"]

            .get(difficulty,1)

            *

            total_questions

        )


        if difficulty_count.get(
            difficulty,0
        ) >= max_allowed:

            return False




        # -----------------------------
        # Bloom Check
        # -----------------------------


        max_allowed = (

            self.rules["bloom_distribution"]

            .get(bloom,1)

            *

            total_questions

        )


        if bloom_count.get(
            bloom,0
        ) >= max_allowed:

            return False




        # -----------------------------
        # Unit Coverage Check
        # -----------------------------


        max_allowed = (

            self.rules["unit_distribution"]

            .get(unit,1)

            *

            total_questions

        )


        if unit_count.get(
            unit,0
        ) >= max_allowed:

            return False



        return True





    def _update_count(

        self,

        question,

        difficulty_count,

        bloom_count,

        unit_count

    ):


        difficulty = question.get(
            "difficulty"
        )


        bloom = question.get(
            "bloom_level"
        )


        unit = question.get(
            "unit"
        )



        difficulty_count[difficulty] = (

            difficulty_count.get(
                difficulty,0
            ) + 1

        )



        bloom_count[bloom] = (

            bloom_count.get(
                bloom,0
            ) + 1

        )



        unit_count[unit] = (

            unit_count.get(
                unit,0
            ) + 1

        )