from collections import defaultdict


class TemplateAnalyzer:

    def analyze(self, extracted):

        questions = extracted["questions"]

        grouped = defaultdict(list)

        total_marks = 0

        sections = {}

        choices = 0

        for q in questions:

            grouped[q["question_no"]].append(q)

            total_marks += q["marks"]

            if q["has_choice"]:
                choices += 1

            section = q["section"]

            if section not in sections:

                sections[section] = {

                    "questions": 0,

                    "marks": 0

                }

            sections[section]["questions"] += 1

            sections[section]["marks"] += q["marks"]

        return {

            "total_questions": len(questions),

            "unique_questions": len(grouped),

            "total_marks": total_marks,

            "sections": sections,

            "optional_questions": choices,

            "pattern": dict(grouped)

        }