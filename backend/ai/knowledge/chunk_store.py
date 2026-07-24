from pathlib import Path
import json


SAVE_DIR = Path("storage/chunks")

SAVE_DIR.mkdir(

    parents=True,

    exist_ok=True

)


def save_chunks(

    filename,

    chunks

):

    data = []

    for i, chunk in enumerate(chunks):

        data.append({

            "chunk_id": i + 1,

            "text": chunk

        })

    output = SAVE_DIR / f"{filename}.json"

    with open(

        output,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )

    return output