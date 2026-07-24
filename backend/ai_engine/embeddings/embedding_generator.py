"""
embedding_generator.py

Generate MiniLM embeddings for text chunks.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self):

        print("Loading MiniLM model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("MiniLM Loaded Successfully!")

    def generate_embedding(self, text: str):

        """
        Generate embedding for a single text chunk.
        """

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding.tolist()

    def generate_embeddings(self, chunks):

        """
        Generate embeddings for multiple chunks.
        """

        embeddings = []

        for chunk in chunks:

            vector = self.generate_embedding(chunk)

            embeddings.append(vector)

        return embeddings