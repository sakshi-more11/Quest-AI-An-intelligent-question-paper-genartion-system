"""
pattern_extractor.py

Extracts examination paper structure from Previous Year Papers.
"""

import re


class PatternExtractor:

    def __init__(self):

        self.question_pattern = re.compile(
            r'(?:Q(?:uestion)?\.?\s*)?(\d+)'
            r'\s*'
            r'(?:[\(\[]?([a-zA-Z])[\)\]]?)?'
            r'.*?'
            r'(\d+)\s*(?:Marks?|Mark|M\b)',
            re.IGNORECASE
        )

        self.section_pattern = re.compile(
            r'SECTION\s*[-:]?\s*([A-Z])',
            re.IGNORECASE
        )

        self.choice_pattern = re.compile(
            r'\b(OR|Either|Attempt\s+Any|Any\s+Two|Any\s+Three)\b',
            re.IGNORECASE
        )

    def extract(self, text):

        sections = self.extract_sections(text)

        questions = []

        current_section = "General"
        current_question_no = None
        current_choice = False

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            section_match = self.section_pattern.search(line)

            if section_match:

                current_section = section_match.group(1)

                continue

            # University templates commonly put "Q.1" on one line and
            # "a) ... 8 Marks" on the next line/table cell.  Keep the parent
            # question number while reading those sub-question lines.
            parent = re.match(r"^\s*(?:Q(?:uestion)?\.?\s*)?(\d+)\s*[\.)]?(?:\s|$)", line, re.IGNORECASE)
            if parent:
                current_question_no = parent.group(1)
            if self.choice_pattern.search(line):
                current_choice = True

            question_match = self.question_pattern.search(line)
            subpart = re.match(r"^\s*(?:\(?([a-zA-Z])\)?\s*[\)\.\:]|\(([a-zA-Z])\))", line)
            marks_match = re.search(r"\b(\d+)\s*(?:Marks?|Mark|M\b)", line, re.IGNORECASE)

            if question_match:
                question_no = question_match.group(1)
                current_question_no = question_no
                sub_question = question_match.group(2) or ((subpart.group(1) or subpart.group(2)) if subpart else "")
                marks = int(question_match.group(3))
            elif current_question_no and subpart and marks_match:
                question_no = current_question_no
                sub_question = subpart.group(1) or subpart.group(2)
                marks = int(marks_match.group(1))
            else:
                continue

            questions.append({
                "section": current_section,
                "question_no": question_no,
                "sub_question": sub_question,
                "marks": marks,
                "has_choice": current_choice,
            })
            # OR applies to the next alternative only; do not contaminate all
            # later questions in the paper.
            current_choice = False

        return {

            "sections": sections,

            "questions": questions

        }

    def extract_sections(self, text):

        matches = self.section_pattern.findall(text)

        if not matches:

            return ["General"]

        return list(dict.fromkeys(matches))
