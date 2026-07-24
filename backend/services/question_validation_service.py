from backend.ai.validation.bloom_classifier import predict_bloom

from backend.ai.validation.difficulty_classifier import predict_difficulty

from backend.ai.validation.duplicate_detector import is_duplicate



class QuestionValidationService:



    def validate(

        self,

        questions,

        existing_questions

    ):


        validated=[]


        for q in questions:


            question_text = q["question"]



            if is_duplicate(

                question_text,

                existing_questions

            ):

                continue



            q["predicted_bloom"] = predict_bloom(

                question_text

            )


            q["predicted_difficulty"] = predict_difficulty(

                question_text

            )



            validated.append(q)



        return validated