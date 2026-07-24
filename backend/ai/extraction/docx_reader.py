from docx import Document


def extract_docx_text(file_path: str) -> str:

    document = Document(file_path)

    paragraphs = []

    for para in document.paragraphs:

        if para.text.strip():

            paragraphs.append(para.text)

    return "\n".join(paragraphs)