"""Constraint-aware, deterministic selection from the verified question bank."""

from difflib import SequenceMatcher


class QuestionSelector:
    def __init__(self, duplicate_threshold=0.88):
        self.duplicate_threshold = duplicate_threshold

    def select(self, question_pool, marks_distribution, syllabus_topics=None):
        required = self._requirements(marks_distribution)
        candidates = self._deduplicate(question_pool)
        selected, used_topics = [], set()
        for marks in sorted(required, reverse=True):
            for _ in range(required[marks]):
                # Template marks describe the slot, not a prerequisite on
                # the stored question.  The selected question is assigned
                # the slot mark later by TemplateApplier.
                choices = [question for question in candidates if question not in selected]
                if not choices:
                    continue
                # Coverage first, then preserve a varied Bloom/difficulty mix, then stable text order.
                choices.sort(key=lambda question: (
                    str(question.get("topic") or question.get("unit")) in used_topics,
                    sum(existing.get("bloom_level") == question.get("bloom_level") for existing in selected),
                    sum(existing.get("difficulty") == question.get("difficulty") for existing in selected),
                    str(question.get("question", "")).lower(),
                ))
                choice = choices[0]
                selected.append(choice)
                used_topics.add(str(choice.get("topic") or choice.get("unit") or ""))
        return selected

    @staticmethod
    def _requirements(distribution):
        if isinstance(distribution, dict):
            return {int(marks): int(count) for marks, count in distribution.items()}
        result = {}
        for marks in distribution:
            result[int(marks)] = result.get(int(marks), 0) + 1
        return result

    def _deduplicate(self, questions):
        unique = []
        for question in questions:
            text = str(question.get("question", "")).strip()
            if text and all(SequenceMatcher(None, text.lower(), str(old.get("question", "")).lower()).ratio() < self.duplicate_threshold for old in unique):
                unique.append(question)
        return unique
