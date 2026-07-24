"""Learn question slots from selectable university-paper templates.

Scanned papers need stateful parsing because OCR commonly puts ``Q.2``,
``a)`` and ``7 Marks`` on three different lines.
"""

import re


class TemplateParser:
    _section = re.compile(r"^\s*(?:SECTION|PART)\s*[-:. ]*([A-Z0-9IVX]+)\b", re.I)
    # A bare number is only a question label when it has punctuation. This
    # prevents table values such as ``2`` and ``3 Boosting`` becoming Q.2/Q.3.
    _question = re.compile(r"^\s*(?:Q(?:UESTION)?\s*\.?\s*(\d{1,2})|(\d{1,2})\s*[.)-])(?:\s|$)", re.I)
    _subquestion = re.compile(r"^\s*\(?([a-c])\)?\s*[.)-]\s*$", re.I)
    _inline_subquestion = re.compile(r"^\s*(?:Q(?:UESTION)?\s*\.?\s*\d+\s*)?\(?([a-c])\)?\s*[.)-]\s+", re.I)
    _marks = re.compile(r"(?:\[\s*(\d{1,2})\s*\]|\(\s*(\d{1,2})\s*\)|\b(\d{1,2})\s*(?:marks?|m\b)|:\s*(\d{1,2})\s*$)", re.I)
    _or = re.compile(r"^\s*(?:[-–—]\s*)?(?:OR|EITHER\s*/?\s*OR)\s*$", re.I)

    def __init__(self):
        self.processor = None

    def parse(self, file_path):
        if self.processor is None:
            from backend.ai_engine.preprocessing.document_processor import DocumentProcessor
            self.processor = DocumentProcessor()
        document = self.processor.process(file_path)
        slots = self._slots(document.get("text", ""))
        if not slots:
            raise ValueError("No question slots and marks could be read from the uploaded template.")
        pattern = {}
        for slot in slots:
            pattern.setdefault(slot["question_no"], []).append(slot)
        return {"text": document["text"], "learned_template": {"pattern": pattern, "slots": slots}}

    def _slots(self, text):
        slots, section = [], "General"
        question_no, sub_question, next_auto_question = None, None, 1
        pending_or, choice_number = False, 0

        def add_slot(marks):
            nonlocal pending_or, choice_number
            if question_no is None or sub_question is None or not 1 <= marks <= 20:
                return
            choice_group = None
            if (pending_or and slots and slots[-1]["question_no"] == str(question_no)
                    and slots[-1]["sub_question"] == sub_question):
                choice_number += 1
                choice_group = f"choice-{choice_number}"
                # The alternative follows OR. Pair it to the prior slot; a
                # missing OCR mark on that prior slot is repaired below.
                slots[-1]["choice_group"] = choice_group
                pending_or = False
            slots.append({"section": section, "question_no": str(question_no),
                          "sub_question": sub_question, "marks": marks,
                          **({"choice_group": choice_group} if choice_group else {})})

        lines = [" ".join(raw.split()) for raw in text.splitlines()]
        for line in lines:
            if not line:
                continue
            section_match = self._section.match(line)
            if section_match:
                section, question_no, sub_question = section_match.group(1).upper(), None, None
                continue
            if self._or.match(line):
                pending_or = True
                sub_question = None
                continue

            question_match = self._question.match(line)
            if question_match:
                question_no = int(question_match.group(1) or question_match.group(2))
                next_auto_question = max(next_auto_question, question_no + 1)
                sub_question = None
                # OCR can keep a sub-label on the same line as Q.2.
                remainder = line[question_match.end():]
                inline = self._inline_subquestion.match(remainder)
                if inline:
                    sub_question = inline.group(1).lower()
            else:
                label = self._subquestion.match(line) or self._inline_subquestion.match(line)
                if label:
                    # First table entry in many scans loses the "1" in Q.1.
                    if question_no is None:
                        question_no = next_auto_question
                        next_auto_question += 1
                    sub_question = label.group(1).lower()

            mark_match = self._marks.search(line)
            if mark_match:
                marks = next(int(value) for value in mark_match.groups() if value)
                # Ignore header metadata such as "Max Marks: 100" and marks
                # embedded inside an already parsed question's explanatory text.
                add_slot(marks)

        # An OCR row can omit the mark for the first side of an OR pair while
        # reading the alternative correctly. Both alternatives share the mark.
        for index, slot in enumerate(slots):
            group = slot.get("choice_group")
            if group and index + 1 < len(slots) and slots[index + 1].get("choice_group") == group:
                if not slot["marks"]:
                    slot["marks"] = slots[index + 1]["marks"]
        return self._deduplicate(slots)

    @staticmethod
    def _deduplicate(slots):
        """Drop OCR duplicates but retain explicit OR alternatives."""
        result, seen = [], set()
        for slot in slots:
            key = (slot["section"], slot["question_no"], slot["sub_question"], slot.get("choice_group"))
            if key in seen:
                # Repeated mark OCR should not create another question slot.
                continue
            seen.add(key)
            result.append(slot)
        return result
