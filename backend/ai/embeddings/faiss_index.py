import faiss
import numpy as np
import pickle
from pathlib import Path


VECTOR_DIR = Path("storage/vector_db")

VECTOR_DIR.mkdir(

    parents=True,

    exist_ok=True

)


def build_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        embeddings
    )

    return index


def save_index(index):

    faiss.write_index(

        index,

        str(VECTOR_DIR / "knowledge.index")
    )


def save_metadata(chunks):

    with open(

        VECTOR_DIR / "chunks.pkl",

        "wb"

    ) as f:

        pickle.dump(

            chunks,

            f
        )


def load_index():

    return faiss.read_index(

        str(VECTOR_DIR / "knowledge.index")
    )


def load_chunks():

    with open(

        VECTOR_DIR / "chunks.pkl",

        "rb"

    ) as f:

        return pickle.load(f)

def search(

    query_embedding,

    index,

    chunks,

    top_k=5

):

    distances, indices = index.search(

        np.array([query_embedding]),

        top_k

    )

    results = []

    for idx in indices[0]:

        results.append(

            chunks[idx]

        )

    return results    