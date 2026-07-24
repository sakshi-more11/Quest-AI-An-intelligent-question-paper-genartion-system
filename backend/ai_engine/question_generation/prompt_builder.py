"""
prompt_builder.py

Builds prompts for engineering question generation.
"""


class PromptBuilder:

    def build(
        self,
        subject,
        unit,
        bloom_level,
        difficulty,
        marks,
        question_type,
        context,
        number_of_questions=1
    ):

        prompt = f"""
You are an experienced university professor responsible for preparing engineering university examination papers.

Generate exactly {number_of_questions} examination question(s).

=========================
QUESTION REQUIREMENTS
=========================

Subject:
{subject}

Unit:
{unit}

Bloom's Taxonomy Level:
{bloom_level}

Difficulty:
{difficulty}

Marks:
{marks}

Question Type:
{question_type}

=========================
REFERENCE CONTEXT
=========================

{context}

=========================
STRICT RULES
=========================

1. Use ONLY the information present in the Reference Context.
2. Never invent facts or topics.
3. Questions must be suitable for engineering university examinations.
4. Follow the requested Bloom's Taxonomy level exactly.
5. Match the requested difficulty level.
6. Match the requested marks.
7. Avoid duplicate questions.
8. Do NOT generate answers.
9. Do NOT generate explanations.
10. Do NOT generate solutions.
11. Do NOT generate marking schemes.
12. Do NOT use markdown.
13. Do NOT use headings.
14. Do NOT mention Bloom's Taxonomy in the output.
15. Do NOT mention difficulty level in the output.
16. Do NOT mention "Reference Context".
17. Every question should be clear, grammatically correct and complete.
18. If the context is insufficient, generate the closest possible valid question only from the available context.

=========================
OUTPUT FORMAT
=========================

Return ONLY a valid JSON object with a "questions" array.

Example:

{{
  "questions": [
    {{
        "question": "Explain the working of Decision Tree algorithm with a suitable example.",
        "marks": {marks},
        "difficulty": "{difficulty}",
        "bloom_level": "{bloom_level}",
        "unit": "{unit}",
        "question_type": "{question_type}"
    }}
  ]
}}

Return ONLY JSON.

Do not write anything before or after the JSON.
"""

        return prompt.strip()
