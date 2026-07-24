import pdfplumber


def extract_pdf(file_path: str):

    text = []

    with pdfplumber.open(file_path) as pdf:

            print("TOTAL PAGES:", len(pdf.pages))

            for i, page in enumerate(pdf.pages):

                page_text = page.extract_text()

                print("PAGE", i + 1)
                print(repr(page_text))

                if page_text:
                    text += page_text + "\n"

                pages.append({
                    "page_number": i + 1,
                    "text": page_text or ""
                })