class QuestionRenderer:


    def render(self, questions):

        output=[]


        current_question=None


        for q in questions:


            if q.get(
                "question_number"
            ) != current_question:


                current_question = q.get(
                    "question_number"
                )


                output.append(
                    f"\nQ.{current_question}"
                )


            output.append(
                q["text"]
            )


            output.append(
                f"Marks: {q.get('marks','')}"
            )


            output.append(
                f"CO: {q.get('co','')}"
            )


            output.append(
                f"BL: {q.get('bloom_level','')}"
            )


            output.append(
                ""
            )


        return output