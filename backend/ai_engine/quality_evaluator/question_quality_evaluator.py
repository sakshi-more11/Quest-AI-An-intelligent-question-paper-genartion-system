"""
question_quality_evaluator.py

Evaluates generated questions.
"""


from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



class QuestionQualityEvaluator:



    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )



    def evaluate(

        self,

        question,

        context,

        expected_bloom,

        expected_difficulty

    ):


        syllabus_score = self._syllabus_score(

            question,

            context

        )


        bloom_score = self._bloom_score(

            question,

            expected_bloom

        )


        difficulty_score = self._difficulty_score(

            question,

            expected_difficulty

        )


        clarity_score = self._clarity_score(

            question

        )



        overall = (

            syllabus_score +

            bloom_score +

            difficulty_score +

            clarity_score

        ) / 4



        return {


            "question":question,


            "scores":{


                "syllabus":

                syllabus_score,


                "bloom":

                bloom_score,


                "difficulty":

                difficulty_score,


                "clarity":

                clarity_score

            },


            "overall_score":

            round(overall,2),


            "status":

            "Accepted"

            if overall >=70

            else

            "Rejected"

        }




    def _syllabus_score(

        self,

        question,

        context

    ):


        q_embedding = self.model.encode(
            question
        )


        c_embedding = self.model.encode(
            context
        )


        similarity = cosine_similarity(

            [q_embedding],

            [c_embedding]

        )[0][0]


        return round(

            similarity*100,

            2

        )



    def _bloom_score(

        self,

        question,

        bloom

    ):


        keywords={


        "Remember":

        ["define","list","state"],


        "Understand":

        ["explain","describe"],


        "Apply":

        ["apply","solve","use"],


        "Analyze":

        ["analyze","compare","differentiate"]


        }


        words = keywords.get(

            bloom,

            []

        )


        for word in words:

            if word.lower() in question.lower():

                return 90



        return 60




    def _difficulty_score(

        self,

        question,

        difficulty

    ):


        length=len(
            question.split()
        )


        if difficulty=="Hard" and length>15:

            return 90


        if difficulty=="Medium" and length>10:

            return 85


        if difficulty=="Easy":

            return 90


        return 60




    def _clarity_score(

        self,

        question

    ):


        if len(question.split())>=5:

            return 90


        return 50