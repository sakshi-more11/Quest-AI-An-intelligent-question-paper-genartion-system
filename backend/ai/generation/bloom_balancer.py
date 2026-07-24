"""
QuestAI Bloom Taxonomy Balancer

Balances questions according to
Bloom's Taxonomy distribution.
"""

from collections import defaultdict


class BloomBalancer:


    def balance(
        self,
        questions,
        rules
    ):

        grouped = defaultdict(list)

        for q in questions:
            grouped[q["bl"]].append(q)

        total_questions = rules["question_count"]

        distribution = rules["bloom_distribution"]

        required = {}

        for level, percent in distribution.items():

            required[level] = round(
                total_questions * percent / 100
            )

        balanced = []

        selected_ids = set()

        for level in distribution.keys():

            available = grouped[level]

            count = min(

                required[level],

                len(available)

            )

            for q in available[:count]:

                balanced.append(q)

                selected_ids.add(q["id"])

        remaining = total_questions - len(balanced)

        if remaining > 0:

            leftovers = []

            for level in distribution.keys():

                for q in grouped[level]:

                    if q["id"] not in selected_ids:

                        leftovers.append(q)

            balanced.extend(
                leftovers[:remaining]
            )

        return balanced