import random


class QuestionSelector:

    def __init__(self, questions):
        self.questions = questions

    # -----------------------------
    # Subject Filter
    # -----------------------------

    def filter_subject(self, subject):

        return [
            q
            for q in self.questions
            if q.subject == subject
        ]

    # -----------------------------
    # Unit Filter
    # -----------------------------

    def filter_units(self, questions, units):

        return [
            q
            for q in questions
            if q.unit in units
        ]

    # -----------------------------
    # Bloom Filter
    # -----------------------------

    def filter_bloom(self, questions, bloom):

        return [
            q
            for q in questions
            if q.bloom == bloom
        ]

    # -----------------------------
    # Difficulty Filter
    # -----------------------------

    def filter_difficulty(self, questions, difficulty):

        return [
            q
            for q in questions
            if q.difficulty == difficulty
        ]

    # -----------------------------
    # Marks Filter
    # -----------------------------

    def filter_marks(self, questions, marks):

        return [
            q
            for q in questions
            if q.marks == marks
        ]

    # -----------------------------
    # Intelligent Selection
    # -----------------------------

    def choose_intelligent(
        self,
        questions,
        count,
        used_ids=None
    ):

        if used_ids is None:
            used_ids = set()

        scored_questions = []

        covered_units = set()
        covered_bloom = set()
        covered_difficulty = set()

        for q in questions:

            qid = getattr(q, "id", id(q))

            if qid in used_ids:
                continue

            score = 0

            if q.unit not in covered_units:
                score += 5

            if q.bloom not in covered_bloom:
                score += 4

            if q.difficulty not in covered_difficulty:
                score += 3

            scored_questions.append((score, q))

        scored_questions.sort(
            key=lambda x: x[0],
            reverse=True
        )

        selected = []

        for score, q in scored_questions:

            if len(selected) >= count:
                break

            qid = getattr(q, "id", id(q))

            if qid in used_ids:
                continue

            selected.append(q)

            used_ids.add(qid)

            covered_units.add(q.unit)
            covered_bloom.add(q.bloom)
            covered_difficulty.add(q.difficulty)

        return selected