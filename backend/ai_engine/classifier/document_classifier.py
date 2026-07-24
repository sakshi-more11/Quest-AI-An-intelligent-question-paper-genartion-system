from pathlib import Path

from backend.ai_engine.classifier.patterns import DOCUMENT_PATTERNS
from backend.ai_engine.classifier.document_types import DocumentType


class DocumentClassifier:

    def classify(self, text, filename="", file_type=""):

        text = text.lower()

        path = Path(filename)

        filename = path.stem.lower()

        extension = path.suffix.lower()

        file_type = file_type.lower()

        scores = {doc_type: 0 for doc_type in DOCUMENT_PATTERNS}

        # =====================================================
        # 1. Filename Based Scoring
        # =====================================================

        if any(word in filename for word in [
            "syllabus", "curriculum", "course", "scheme"
        ]):
            scores["SYLLABUS"] += 8

        if any(word in filename for word in [
            "notes", "lecture", "module", "handout"
        ]):
            scores["LECTURE_NOTES"] += 8

        if any(word in filename for word in [
            "question", "paper", "midsem", "endsem", "exam"
        ]):
            scores["PREVIOUS_YEAR_PAPER"] += 8

        if any(word in filename for word in [
            "lab", "manual", "experiment"
        ]):
            scores["LAB_MANUAL"] += 8

        if any(word in filename for word in [
            "book", "reference", "textbook"
        ]):
            scores["REFERENCE_BOOK"] += 8

        if any(word in filename for word in [
            "slides", "presentation", "ppt"
        ]):
            scores["PPT_SLIDES"] += 8

        # =====================================================
        # 2. Extension Based Scoring
        # =====================================================

        if extension in [".ppt", ".pptx"] or file_type in ["ppt", "pptx"]:
            scores["PPT_SLIDES"] += 5

        if extension in [".doc", ".docx"] or file_type in ["doc", "docx"]:
            scores["LECTURE_NOTES"] += 2

        # =====================================================
        # 3. Content Based Scoring
        # =====================================================

        for doc_type, keywords in DOCUMENT_PATTERNS.items():

            for keyword in keywords:

                if keyword.lower() in text:

                    # Give more importance to meaningful phrases
                    if len(keyword.split()) >= 2:
                        scores[doc_type] += 3
                    else:
                        scores[doc_type] += 1

        # =====================================================
        # Final Decision
        # =====================================================

        best_match = max(scores, key=scores.get)

        best_score = scores[best_match]

        total_score = sum(scores.values())

        if best_score == 0 or total_score == 0:

            return {
                "document_type": DocumentType.UNKNOWN.value,
                "confidence": 0.0
            }

        # If the filename strongly indicates the document type,
# prefer that over content keywords.

        if "syllabus" in filename:
            best_match = "SYLLABUS"

        elif any(word in filename for word in ["question", "paper", "midsem", "endsem", "exam"]):
            best_match = "PREVIOUS_YEAR_PAPER"

        elif any(word in filename for word in ["notes", "lecture", "module"]):
            best_match = "LECTURE_NOTES"

        elif any(word in filename for word in ["slides", "ppt", "presentation"]):
            best_match = "PPT_SLIDES"

        elif any(word in filename for word in ["lab", "manual"]):
            best_match = "LAB_MANUAL"

        elif any(word in filename for word in ["book", "reference"]):
            best_match = "REFERENCE_BOOK"

        confidence = round(best_score / total_score, 2)

        return {
            "document_type": DocumentType[best_match].value,
            "confidence": confidence
        }