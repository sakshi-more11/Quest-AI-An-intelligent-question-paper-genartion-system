"""
duplicate_checker.py

Checks duplicate generated questions.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class DuplicateChecker:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def remove_duplicates(

        self,

        questions,

        threshold=0.90

    ):

        unique = []

        embeddings = []

        for item in questions:

            # Support both JSON and string format
            if isinstance(item, dict):

                question = item.get("question", "")

            else:

                question = str(item)

            emb = self.model.encode(question)

            duplicate = False

            for old in embeddings:

                score = cosine_similarity(

                    [emb],

                    [old]

                )[0][0]

                if score >= threshold:

                    duplicate = True

                    break

            if not duplicate:

                unique.append(item)

                embeddings.append(emb)

        return unique