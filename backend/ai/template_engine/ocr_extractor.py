import easyocr
import fitz


class OCRExtractor:


    def __init__(self):

        self.reader = easyocr.Reader(
            ['en']
        )


    def extract_from_pdf(self, file_path):

        document = fitz.open(file_path)

        pages = []


        for page_number, page in enumerate(document):

            pix = page.get_pixmap(
                dpi=300
            )


            image_path = (
                f"temp_page_{page_number}.png"
            )


            pix.save(image_path)


            result = self.reader.readtext(
                image_path
            )


            blocks = []


            for item in result:

                bbox, text, confidence = item


                blocks.append({

                    "text": text,

                    "bbox": bbox,

                    "confidence": confidence,

                    "page":
                    page_number + 1

                })


            pages.append({

                "page_number":
                page_number + 1,

                "blocks":
                blocks

            })


        document.close()


        return {

            "total_pages":
            len(pages),

            "pages":
            pages

        }