from collections import Counter

from backend.ai.paper_generation.similarity import is_similar


class PaperValidator:

    def validate(

        self,

        blueprint,

        questions

    ):

        report = {}

        # ------------------------
        # Unit Coverage
        # ------------------------

        expected_units = set(blueprint.units)

        obtained_units = set(
            q.unit
            for q in questions
        )

        report["unit_coverage"] = round(

            len(

                expected_units.intersection(
                    obtained_units
                )

            )

            /

            len(expected_units)

            *

            100,

            2

        )

        # ------------------------
        # Bloom Distribution
        # ------------------------

        bloom_counter = Counter(

            q.bloom

            for q in questions

        )

        report["bloom_distribution"] = dict(

            bloom_counter

        )

        # ------------------------
        # Difficulty Distribution
        # ------------------------

        difficulty_counter = Counter(

            q.difficulty

            for q in questions

        )

        report["difficulty_distribution"] = dict(

            difficulty_counter

        )

        # ------------------------
        # Duplicate Detection
        # ------------------------

        texts = []

        duplicates = 0

        for q in questions:

            if q.question_text in texts:

                duplicates += 1

            texts.append(q.question_text)

        report["duplicates"] = duplicates

        # ------------------------
        # Similar Questions
        # ------------------------

        similar = 0

        for i in range(len(questions)):

            for j in range(i + 1, len(questions)):

                if is_similar(

                    questions[i].question_text,

                    questions[j].question_text

                ):

                    similar += 1

        report["similar_questions"] = similar

        # ------------------------
        # Marks Validation
        # ------------------------

        total_marks = sum(

            q.marks

            for q in questions

        )

        report["total_marks"] = total_marks

        report["expected_marks"] = blueprint.total_marks

        report["marks_valid"] = (

            total_marks

            ==

            blueprint.total_marks

        )

        # ------------------------
        # Overall Score
        # ------------------------

        score = 100

        score -= duplicates * 10

        score -= similar * 5

        if not report["marks_valid"]:

            score -= 20

        report["quality_score"] = max(

            score,

            0

        )

        return report