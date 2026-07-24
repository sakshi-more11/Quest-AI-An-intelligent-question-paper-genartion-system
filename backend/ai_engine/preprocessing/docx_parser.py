"""
docx_parser.py

Extract text from Microsoft Word (.docx) documents.
"""

from pathlib import Path
from docx import Document


class DOCXParser:

    def extract(self, docx_path: str) -> dict:

        docx_path = Path(docx_path)

        if not docx_path.exists():
            raise FileNotFoundError(f"{docx_path} not found.")

        document = Document(docx_path)

        paragraphs = []

        for para in document.paragraphs:

            text = para.text.strip()

            if text:
                paragraphs.append(text)

        full_text = "\n".join(paragraphs)

        return {
            "filename": docx_path.name,
            "file_type": "docx",
            "pages": 1,          # DOCX has no fixed pages
            "text": full_text,
            "page_data": [
                {
                    "page": 1,
                    "text": full_text
                }
            ]
        }