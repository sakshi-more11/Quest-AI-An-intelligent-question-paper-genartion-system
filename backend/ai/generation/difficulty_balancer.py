"""
QuestAI Difficulty Balancer

Balances questions according to
difficulty distribution.
"""

from collections import defaultdict


class DifficultyBalancer:


    def balance(
        self,
        questions,
        rules
    ):


        grouped = defaultdict(list)


        for q in questions:

            grouped[q["difficulty"]].append(q)


        total_questions = rules["question_count"]

        distribution = rules["difficulty_distribution"]


        required = {

            "easy": round(
                total_questions *
                distribution["easy"] / 100
            ),

            "medium": round(
                total_questions *
                distribution["medium"] / 100
            ),

            "hard": round(
                total_questions *
                distribution["hard"] / 100
            )

        }


        balanced = []


        for level in [

            "easy",

            "medium",

            "hard"

        ]:


            available = grouped[level]


            count = min(

                required[level],

                len(available)

            )


            balanced.extend(

                available[:count]

            )


        remaining = total_questions - len(balanced)


        if remaining > 0:


            leftovers = []


            for level in [

                "easy",

                "medium",

                "hard"

            ]:


                leftovers.extend(

                    grouped[level][required[level]:]

                )


            balanced.extend(

                leftovers[:remaining]

            )


        return balanced