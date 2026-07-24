"""
faiss_manager.py

QuestAI Semantic Vector Database

Responsibilities:

1. Receive knowledge records
2. Generate embeddings using Sentence Transformer
3. Build FAISS cosine similarity index
4. Perform semantic search
5. Save / Load vector database

Phase:
10.3 Knowledge Base Creation
"""

import os
import pickle

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer



class FAISSManager:


    def __init__(self):


        # Sentence Transformer model
        # 384 dimensional embeddings

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )


        self.dimension = 384



        # Cosine similarity index

        self.index = faiss.IndexFlatIP(
            self.dimension
        )



        # Original documents

        self.records = []



    # ==================================================
    # Build FAISS Index
    # ==================================================

    def build_index(self, knowledge_records):


        print("==============================")
        print("FAISS BUILD DEBUG")
        print("Input records:", len(knowledge_records))
        print("==============================")


        # Reset index every build

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.records = []


        texts = []


        for record in knowledge_records:


            print("PROCESSING RECORD:")
            print(record)


            # Handle dictionary

            if isinstance(record, dict):

                text = (
                    record.get("text")
                    or
                    record.get("content")
                    or
                    ""
                )


            else:

                text = str(record)



            if text.strip():

                texts.append(text)


                self.records.append(
                    {
                        "text": text
                    }
                )


        print("==============================")
        print(
            "FINAL TEXT COUNT:",
            len(texts)
        )

        print(
            "FINAL RECORD COUNT:",
            len(self.records)
        )

        print("==============================")


        if not texts:

            print(
                "No text available"
            )

            return



        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True
        )


        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )


        faiss.normalize_L2(
            embeddings
        )


        self.index.add(
            embeddings
        )


        print(
            f"{len(embeddings)} embeddings indexed."
        )



    # ==================================================
    # Semantic Search
    # ==================================================

    def search(
            self,
            query,
            top_k=5
        ):

            if self.index.ntotal == 0:
                print("FAISS index empty.")
                return []

            query_embedding = self.embedding_model.encode(
                [query],
                convert_to_numpy=True
            )

            query_embedding = np.array(
                query_embedding,
                dtype=np.float32
            )

            faiss.normalize_L2(query_embedding)

            scores, indices = self.index.search(
                query_embedding,
                top_k
            )

            results = []

            for score, idx in zip(scores[0], indices[0]):

                if idx == -1:
                    continue

                results.append({
                    "score": float(score),
                    "record": self.records[idx]
                })

            return results


        # ==================================================
        # Return All Knowledge Chunks
        # ==================================================

    def get_all_chunks(self):

            return [
                record["text"]
                for record in self.records
            ]

    # ==================================================
    # Save FAISS Database
    # ==================================================

    def save(
        self,
        folder
    ):


        os.makedirs(

            folder,

            exist_ok=True

        )



        faiss.write_index(

            self.index,

            os.path.join(

                folder,

                "knowledge.index"

            )

        )



        with open(

            os.path.join(

                folder,

                "records.pkl"

            ),

            "wb"

        ) as file:


            pickle.dump(

                self.records,

                file

            )



        print(
            "FAISS index saved successfully."
        )



    # ==================================================
    # Load FAISS Database
    # ==================================================

    def load(
        self,
        folder
    ):



        index_path = os.path.join(

            folder,

            "knowledge.index"

        )


        record_path = os.path.join(

            folder,

            "records.pkl"

        )



        if not os.path.exists(index_path):


            raise FileNotFoundError(

                "knowledge.index not found"

            )



        if not os.path.exists(record_path):


            raise FileNotFoundError(

                "records.pkl not found"

            )



        self.index = faiss.read_index(

            index_path

        )



        with open(

            record_path,

            "rb"

        ) as file:


            self.records = pickle.load(file)



        print(

            f"{len(self.records)} records loaded."

        )