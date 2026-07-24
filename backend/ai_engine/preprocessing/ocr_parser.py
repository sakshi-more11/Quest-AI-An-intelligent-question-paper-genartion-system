"""
ocr_parser.py

Extract text from images using EasyOCR.
"""

from pathlib import Path

import easyocr


class OCRParser:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    def extract(self, image_path: str):

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"{image_path} not found."
            )

        results = self.reader.readtext(str(image_path))

        extracted = []

        for item in results:

            extracted.append(item[1])

        full_text = "\n".join(extracted)

        return {

            "filename": image_path.name,

            "file_type": "image",

            "pages": 1,

            "text": full_text,

            "page_data": [

                {

                    "page": 1,

                    "text": full_text

                }

            ]

        }