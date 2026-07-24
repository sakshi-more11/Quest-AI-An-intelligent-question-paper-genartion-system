"""
Object Classifier

Classifies every extracted object into a logical template element.
"""

import re


class ObjectClassifier:

    def classify(self, coordinate_data):

        pages = []

        for page in coordinate_data["pages"]:

            objects = []

            for obj in page["objects"]:

                text = obj["text"].strip()

                obj["type"] = self.detect_type(text)

                objects.append(obj)

            pages.append({

                "page": page["page"],
                "objects": objects

            })

        return {

            "pages": pages

        }

    # -----------------------------
    # Detect Object Type
    # -----------------------------

    def detect_type(self, text):

        t = text.lower()

        # ---------------- Header ----------------

        if "rajarambapu institute" in t:
            return "college_name"

        if "college" in t:
            return "college_name"

        if "institute" in t:
            return "college_name"

        if "university" in t:
            return "college_name"

        if "department" in t:
            return "department"

        if "end semester examination" in t:
            return "exam_title"

        if "mid semester examination" in t:
            return "exam_title"

        # ---------------- Metadata ----------------

        if "course code" in t:
            return "course_code"

        if "course name" in t:
            return "course_name"

        if "semester" in t:
            return "semester"

        if "time" in t:
            return "time"

        if "max marks" in t:
            return "max_marks"

        if "date" in t:
            return "date"

        # ---------------- Instructions ----------------

        if "instruction" in t:
            return "instruction"

        if "all questions are compulsory" in t:
            return "instruction"

        if "assume suitable data" in t:
            return "instruction"

        if "calculator" in t:
            return "instruction"

        # ---------------- Questions ----------------

        if re.match(r"^q\.?\d+", t):
            return "question_number"

        if re.match(r"^[ab]\)?$", t):
            return "sub_question"

        if t == "or":
            return "or"

        # ---------------- Marks ----------------

        if re.fullmatch(r"\d{1,2}", t):

            value = int(t)

            if value <= 20:
                return "marks"

        # ---------------- CO ----------------

        if re.match(r"co\s*\d+", t):
            return "co"

        # ---------------- Bloom ----------------

        if re.match(r"bl\s*\d+", t):
            return "bl"

        # ---------------- Footer ----------------

        if "page" in t:
            return "page_number"

        if "signature" in t:
            return "signature"

        if "centre" in t:
            return "exam_centre"

        # ---------------- Default ----------------

        return "text"