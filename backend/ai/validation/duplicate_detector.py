"""
Duplicate Question Detection
Using SBERT + FAISS
"""


import numpy as np

import faiss


from sentence_transformers import SentenceTransformer



# ---------------------------------------
# Load Sentence Transformer
# ---------------------------------------


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# ---------------------------------------
# Configuration
# ---------------------------------------

SIMILARITY_THRESHOLD = 0.85



# ---------------------------------------
# Create Embeddings
# ---------------------------------------


def create_embedding(question:str):


    embedding = embedding_model.encode(

        question,

        normalize_embeddings=True

    )


    return embedding



# ---------------------------------------
# Build FAISS Index
# ---------------------------------------


def build_index(question_list):


    embeddings = []


    for q in question_list:

        embeddings.append(
            create_embedding(q)
        )



    embeddings = np.array(
        embeddings
    ).astype("float32")



    dimension = embeddings.shape[1]


    index = faiss.IndexFlatIP(
        dimension
    )


    index.add(
        embeddings
    )


    return index



# ---------------------------------------
# Duplicate Check
# ---------------------------------------


def check_duplicate(

        question,

        existing_questions

):


    if len(existing_questions)==0:

        return {

            "duplicate":False,

            "similarity":0

        }



    index = build_index(
        existing_questions
    )



    query_embedding = create_embedding(
        question
    )


    query_embedding = np.array(
        [query_embedding]
    ).astype("float32")



    scores, indices = index.search(

        query_embedding,

        k=1

    )


    similarity = float(
        scores[0][0]
    )



    is_duplicate = (
        similarity >= SIMILARITY_THRESHOLD
    )



    return {


        "duplicate":is_duplicate,


        "similarity":round(
            similarity,
            3
        ),


        "matched_question":

        existing_questions[
            indices[0][0]
        ]

        if is_duplicate

        else None

    }