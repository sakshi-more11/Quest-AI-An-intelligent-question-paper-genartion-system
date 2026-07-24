"""
question_postprocessor.py

Cleans generated questions.
"""

import re


class QuestionPostProcessor:

    # Raw source material, instructions, and generic lead-ins must never be
    # allowed into the question bank.  They are a common symptom of an LLM
    # returning context instead of a question.
    _BAD_PREFIXES = (
        "explain in detail:", "reference material:", "study material:",
        "course outcomes:", "syllabus", "unit ", "department of ",
        "rajarmbapu", "society's",
    )

    def clean(self, questions):

        cleaned = []

        for item in questions:

            # Support both old string format and new JSON format
            if isinstance(item, dict):

                question = item.get("question", "")

            else:

                question = str(item)

            question = re.sub(
                r"^\d+[\).\s]*",
                "",
                str(question or "")
            )

            question = str(question or "").strip()

            if not question or self._is_invalid(question):
                continue

            if isinstance(item, dict):

                item["question"] = question

                cleaned.append(item)

            else:

                cleaned.append(question)

        return cleaned

    @classmethod
    def _is_invalid(cls, question):
        lowered = question.lower()
        if lowered.startswith(cls._BAD_PREFIXES):
            return True
        # A question needs an interrogative/task verb and should not be a
        # pasted paragraph from a PDF/PPT.
        verbs = ("describe", "discuss", "compare", "analyse", "analyze", "design",
                 "derive", "evaluate", "formulate", "implement", "calculate",
                 "illustrate", "justify", "differentiate", "develop", "write")
        words = question.split()
        return len(words) < 6 or len(words) > 55 or not any(word in lowered for word in verbs)
