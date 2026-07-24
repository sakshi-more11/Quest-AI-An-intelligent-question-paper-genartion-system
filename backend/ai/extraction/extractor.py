import os

from backend.ai.extraction.pdf_reader import extract_pdf_text
from backend.ai.extraction.docx_reader import extract_docx_text
from backend.ai.extraction.ppt_reader import extract_ppt_text


def extract_text(file_path: str):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        return extract_pdf_text(file_path)

    elif extension == ".docx":

        return extract_docx_text(file_path)

    elif extension in [".ppt", ".pptx"]:

        return extract_ppt_text(file_path)

    else:

        raise Exception("Unsupported file format")