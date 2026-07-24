from docx import Document


def extract_docx(file_path: str):

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)