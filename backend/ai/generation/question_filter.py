"""
QuestAI Question Filter

Filters questions from Question Bank
according to generation rules.
"""


class QuestionFilter:


    def filter_questions(
        self,
        questions,
        rules
    ):


        filtered = []


        for q in questions:


            # ------------------------
            # Course
            # ------------------------

            if rules["course_code"]:

                if q["course_code"] != rules["course_code"]:

                    continue


            # ------------------------
            # Unit
            # ------------------------

            if rules["units"]:

                if q["unit"] not in rules["units"]:

                    continue


            # ------------------------
            # Difficulty
            # ------------------------

            difficulty = q.get(
                "difficulty"
            )


            if difficulty not in [

                "easy",
                "medium",
                "hard"

            ]:

                continue


            # ------------------------
            # Bloom
            # ------------------------

            if q["bl"] not in rules[
                "bloom_distribution"
            ]:

                continue


            # ------------------------
            # CO
            # ------------------------

            if rules["co_distribution"]:

                if q["co"] not in rules[
                    "co_distribution"
                ]:

                    continue


            filtered.append(q)


        return filtered