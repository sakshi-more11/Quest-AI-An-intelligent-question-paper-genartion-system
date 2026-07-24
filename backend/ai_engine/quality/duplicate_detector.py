"""
QuestAI Duplicate Question Detector

Removes semantically similar questions
"""

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity



class DuplicateDetector:


    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )



    def remove_duplicates(

        self,

        questions,

        threshold=0.85

    ):


        if len(questions) <= 1:

            return questions



        texts = [

            q.get(
                "question",
                ""
            )

            for q in questions

        ]



        embeddings = self.model.encode(

            texts

        )


        unique_questions = []

        unique_embeddings = []



        for index, embedding in enumerate(
            embeddings
        ):


            is_duplicate = False



            for existing in unique_embeddings:


                score = cosine_similarity(

                    [embedding],

                    [existing]

                )[0][0]



                if score >= threshold:

                    is_duplicate = True

                    break



            if not is_duplicate:


                unique_questions.append(

                    questions[index]

                )


                unique_embeddings.append(

                    embedding

                )



        return unique_questions