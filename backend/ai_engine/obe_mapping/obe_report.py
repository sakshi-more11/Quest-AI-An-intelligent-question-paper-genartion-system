"""
obe_report.py

Generates OBE Summary Report.
"""

from collections import Counter


class OBEReport:


    def generate(self, questions):


        co_counter = Counter()
        po_counter = Counter()
        pso_counter = Counter()
        bloom_counter = Counter()
        difficulty_counter = Counter()
        unit_counter = Counter()


        for q in questions:

            # -------------------------
            # CO
            # -------------------------

            co = q.get("CO")

            if co:
                co_counter[co] += 1


            # -------------------------
            # PO
            # -------------------------

            for po in q.get("PO", []):

                po_counter[po] += 1


            # -------------------------
            # PSO
            # -------------------------

            for pso in q.get("PSO", []):

                pso_counter[pso] += 1


            # -------------------------
            # Bloom
            # -------------------------

            bloom = q.get("bloom_level")

            if bloom:

                bloom_counter[bloom] += 1


            # -------------------------
            # Difficulty
            # -------------------------

            difficulty = q.get("difficulty")

            if difficulty:

                difficulty_counter[difficulty] += 1


            # -------------------------
            # Unit
            # -------------------------

            unit = q.get("unit")

            if unit:

                unit_counter[unit] += 1


        report = {

            "total_questions": len(questions),

            "CO_Coverage": dict(co_counter),

            "PO_Coverage": dict(po_counter),

            "PSO_Coverage": dict(pso_counter),

            "Bloom_Coverage": dict(bloom_counter),

            "Difficulty_Coverage": dict(difficulty_counter),

            "Unit_Coverage": dict(unit_counter)

        }

        return report