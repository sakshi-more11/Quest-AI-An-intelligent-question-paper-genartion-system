"""
pdf_parser.py

Extract text from PDF files and return a standard document object.
"""

from pathlib import Path
import pdfplumber


class PDFParser:

    def extract(self, pdf_path: str) -> dict:

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"{pdf_path} not found.")

        extracted_pages = []

        with pdfplumber.open(pdf_path) as pdf:

            total_pages = len(pdf.pages)

            for page_number, page in enumerate(pdf.pages, start=1):

                text = page.extract_text()

                if text:
                    extracted_pages.append({
                        "page": page_number,
                        "text": text
                    })

        full_text = "\n".join(
            page["text"] for page in extracted_pages
        )

        return {
            "filename": pdf_path.name,
            "file_type": "pdf",
            "pages": total_pages,
            "text": full_text,
            "page_data": extracted_pages
        }