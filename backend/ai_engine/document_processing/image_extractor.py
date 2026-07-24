import easyocr


reader = easyocr.Reader(["en"])


def extract_image(file_path: str):

    result = reader.readtext(file_path)

    text = []

    for item in result:

        text.append(item[1])

    return "\n".join(text)