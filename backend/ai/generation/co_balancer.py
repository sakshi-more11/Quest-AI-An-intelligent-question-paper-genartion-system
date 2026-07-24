"""
QuestAI CO Balancer

Balances questions according to
Course Outcome distribution.
"""

from collections import defaultdict


class COBalancer:


    def balance(
        self,
        questions,
        rules
    ):

        grouped = defaultdict(list)

        for q in questions:
            grouped[q["co"]].append(q)

        total_questions = rules["question_count"]

        distribution = rules.get(
            "co_distribution",
            {}
        )

        # If teacher has not specified CO distribution
        if not distribution:
            return questions

        required = {}

        for co, percent in distribution.items():

            required[co] = round(
                total_questions * percent / 100
            )

        balanced = []

        selected_ids = set()

        for co in distribution.keys():

            available = grouped[co]

            count = min(
                required[co],
                len(available)
            )

            for q in available[:count]:

                balanced.append(q)

                selected_ids.add(q["id"])

        remaining = total_questions - len(balanced)

        if remaining > 0:

            leftovers = []

            for co in grouped:

                for q in grouped[co]:

                    if q["id"] not in selected_ids:

                        leftovers.append(q)

            balanced.extend(
                leftovers[:remaining]
            )

        return balanced