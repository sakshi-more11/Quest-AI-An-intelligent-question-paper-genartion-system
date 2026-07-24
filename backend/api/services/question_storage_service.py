"""
Question Storage Service

Stores AI generated questions
into database.
"""


from backend.models.question import Question



class QuestionStorageService:



    def save_questions(

        self,

        questions,

        subject_id,

        db

    ):


        saved = []



        for q in questions:



            question = Question(


                question_text=q.get(

                    "question",

                    ""

                ),


                unit=q.get(

                    "unit"

                ),


                marks=q.get(

                    "marks",

                    5

                ),


                blooms_level=q.get(

                    "blooms_level"

                ),


                difficulty=q.get(

                    "difficulty"

                ),


                question_type=q.get(

                    "question_type"

                ),


                expected_answer_points=q.get(

                    "expected_answer_points"

                ),


                ai_generated=True,


                subject_id=subject_id

            )


            db.add(question)


            saved.append(question)



        db.commit()



        return saved




question_storage_service = QuestionStorageService()