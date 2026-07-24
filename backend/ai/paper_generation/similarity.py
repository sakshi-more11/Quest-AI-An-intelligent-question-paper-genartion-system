from sentence_transformers import SentenceTransformer

from sentence_transformers import util

model = SentenceTransformer(

    "all-MiniLM-L6-v2"

)


def is_similar(

    question1,

    question2,

    threshold=0.90

):

    emb = model.encode(

        [question1, question2],

        convert_to_tensor=True

    )

    similarity = util.cos_sim(

        emb[0],

        emb[1]

    ).item()

    return similarity > threshold