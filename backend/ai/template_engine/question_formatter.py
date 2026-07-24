"""
QuestAI Smart Question Formatter

Formats generated questions into
university examination style.
"""


class QuestionFormatter:


    def format_questions(self, questions):


        formatted = []


        for q in questions:


            block = {


                "question_number":

                    q["question_no"],


                "instruction":

                    "Answer the following:",


                "sub_questions":[],



                "or":None

            }



            # -------------------------
            # A / B Questions
            # -------------------------

            for part in q["parts"]:


                question = part["question"]


                block["sub_questions"].append(


                    {

                    "label":
                        part["label"],


                    "text":
                        question["text"],


                    "marks":
                        question["marks"],


                    "co":
                        question.get(
                            "co",
                            ""
                        ),


                    "bl":
                        question.get(
                            "bl",
                            ""
                        )

                    }

                )




            # -------------------------
            # OR Question
            # -------------------------


            if q["or"]:


                alt = q["or"]["question"]


                block["or"] = {


                    "label":

                        q["or"]["label"],



                    "text":

                        alt["text"],



                    "marks":

                        alt["marks"],



                    "co":

                        alt.get(
                            "co",
                            ""
                        ),



                    "bl":

                        alt.get(
                            "bl",
                            ""
                        )

                }



            formatted.append(block)



        return formatted



    # --------------------------------
    # Render Text Style
    # --------------------------------


    def display_question(self, question):


        output=[]


        output.append(

            f"Q.{question['question_number']} "
            f"{question['instruction']}"

        )


        for sub in question["sub_questions"]:


            output.append(

                self.format_sub_question(

                    sub

                )

            )



        if question["or"]:


            output.append("")


            output.append(

                "OR"

            )


            output.append(

                self.format_or(

                    question["or"]

                )

            )


        return output




    def format_sub_question(self,sub):


        return (

            f"{sub['label']}) "

            f"{sub['text']}"

            f" "

            f"({sub['marks']})"

            f"       "

            f"CO:{sub['co']} "

            f"BL:{sub['bl']}"

        )



    def format_or(self,or_question):


        return (

            f"{or_question['label']}) "

            f"{or_question['text']}"

            f" "

            f"({or_question['marks']})"

            f"       "

            f"CO:{or_question['co']} "

            f"BL:{or_question['bl']}"

        )