"""
Hybrid Coordinate Extractor

Supports:

1. Digital PDFs (PyMuPDF)
2. Scanned PDFs (OCR)
"""

import fitz

from .ocr_extractor import OCRExtractor


class CoordinateExtractor:

    def extract(self, pdf_path):

        document = fitz.open(pdf_path)

        has_text = False

        for page in document:

            if len(page.get_text().strip()) > 50:
                has_text = True
                break

        document.close()

        if has_text:
            return self.extract_text_pdf(pdf_path)

        return self.extract_scanned_pdf(pdf_path)

    # --------------------------------------------------

    def extract_text_pdf(self, pdf_path):

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document):

            objects = []

            page_dict = page.get_text("dict")

            for block in page_dict["blocks"]:

                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    for span in line["spans"]:

                        objects.append({

                            "text": span["text"],

                            "x": span["bbox"][0],

                            "y": span["bbox"][1],

                            "width": span["bbox"][2] - span["bbox"][0],

                            "height": span["bbox"][3] - span["bbox"][1],

                            "font": span["font"],

                            "font_size": span["size"],

                            "flags": span["flags"]

                        })

            pages.append({

                "page": page_number + 1,

                "objects": objects

            })

        document.close()

        return {

            "pages": pages

        }

    # --------------------------------------------------

    def extract_scanned_pdf(self, pdf_path):

        ocr = OCRExtractor()

        result = ocr.extract_from_pdf(pdf_path)

        pages = []

        for page_index, page in enumerate(result["pages"], start=1):

            objects = []

            for block in page["blocks"]:

                bbox = block["bbox"]

                x = bbox[0][0]
                y = bbox[0][1]

                width = bbox[1][0] - bbox[0][0]

                height = bbox[2][1] - bbox[0][1]

                objects.append({

                    "text": block["text"],

                    "x": x,

                    "y": y,

                    "width": width,

                    "height": height,

                    "font": "Unknown",

                    "font_size": height,

                    "flags": 0,

                    "confidence": block["confidence"]

                })

            pages.append({

                "page": page_index,

                "objects": objects

            })

        return {

            "pages": pages

        }