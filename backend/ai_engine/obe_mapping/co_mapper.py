"""
co_mapper.py

Semantic CO Mapping using Sentence Transformers.
"""


from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



class COMapper:


    def __init__(self, co_descriptions):

        """
        co_descriptions example:

        {
            "CO1":
            "Understand fundamental concepts of Machine Learning",

            "CO2":
            "Apply machine learning algorithms for solving problems",

            "CO3":
            "Analyze and evaluate machine learning models"
        }

        """


        self.co_descriptions = co_descriptions


        print("Loading CO Semantic Model...")


        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )


        self.co_embeddings = {}


        for co, description in self.co_descriptions.items():

            self.co_embeddings[co] = self.model.encode(
                description
            )


        print("CO Semantic Model Loaded!")



    def map_question(self, question):


        question_embedding = self.model.encode(
            question
        )


        best_co = None

        best_score = -1



        for co, embedding in self.co_embeddings.items():


            score = cosine_similarity(

                [question_embedding],

                [embedding]

            )[0][0]



            if score > best_score:

                best_score = score

                best_co = co



        return {

            "CO": best_co,

            "confidence": round(
                float(best_score),
                3
            )

        }



    def map_questions(self, questions):


        results=[]


        for q in questions:


            mapping = self.map_question(
                q["question"]
            )


            q["CO"] = mapping["CO"]

            q["CO_confidence"] = mapping["confidence"]


            results.append(q)



        return results