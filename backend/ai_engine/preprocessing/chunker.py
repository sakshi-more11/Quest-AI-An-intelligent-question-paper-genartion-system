"""
chunker.py

Phase 10.2
Document Text Chunking

Input:
    Clean text

Output:
    List of text chunks
"""


class DocumentChunker:


    def __init__(
        self,
        chunk_size=500,
        overlap=50
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap



    def chunk(
            self,
            text
        ):

            if not text:
                return []


            words = text.split()

            chunks = []

            start = 0


            while start < len(words):

                end = start + self.chunk_size


                chunk_text = " ".join(
                    words[start:end]
                )


                chunks.append(
                    chunk_text
                )


                start = end - self.overlap


            return chunks