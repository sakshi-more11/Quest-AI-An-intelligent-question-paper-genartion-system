"""
Question Similarity Checker

Prevents duplicate questions
"""


from sentence_transformers import SentenceTransformer, util





class SimilarityChecker:



    def __init__(self):


        self.model = SentenceTransformer(

            "all-MiniLM-L6-v2"

        )





    def check_duplicate(

        self,

        questions,

        threshold=0.85

    ):


        if len(questions)<2:

            return False



        texts=[

            q["text"]

            for q in questions

        ]



        embeddings=self.model.encode(

            texts,

            convert_to_tensor=True

        )



        similarity = util.cos_sim(

            embeddings[-1],

            embeddings[:-1]

        )



        if max(similarity[0]) > threshold:


            return True



        return False