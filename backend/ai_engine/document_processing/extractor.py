from pathlib import Path

from .pdf_extractor import extract_pdf
from .docx_extractor import extract_docx
from .ppt_extractor import extract_ppt
from .image_extractor import extract_image
from .text_extractor import extract_txt


def extract_document(file_path: str):

    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":

        return extract_pdf(file_path)

    if suffix == ".docx":

        return extract_docx(file_path)

    if suffix == ".pptx":

        return extract_ppt(file_path)

    if suffix == ".txt":

        return extract_txt(file_path)

    if suffix in [

        ".png",
        ".jpg",
        ".jpeg"

    ]:

        return extract_image(file_path)

    return ""