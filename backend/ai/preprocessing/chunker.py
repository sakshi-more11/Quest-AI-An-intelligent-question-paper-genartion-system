from backend.ai.preprocessing.cleaner import clean_text


def chunk_text(

    text,

    chunk_size=500,

    overlap=100

):

    text = clean_text(text)

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks