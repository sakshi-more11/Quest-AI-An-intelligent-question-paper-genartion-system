"""
QuestAI OR Question Generator

Creates university style question paper.

Structure:

Q1
 A Question
 B Question

 OR

 B Alternative Question


Rules:

1. OR question must have same marks
2. Prefer same CO
3. Prefer same Bloom Level
4. Prefer same Difficulty
5. Prefer same Unit

Used questions are removed.

Improvement:
- Automatically creates id if missing
- Prevents duplicate questions
- Maintains A/B pattern for every question
"""


class ORQuestionGenerator:


    def generate(self, questions):

        print("==============================")
        print("OR GENERATOR INPUT")
        print("==============================")

        for q in questions:
            print(q)

        print("==============================")
        # ---------------------------------
        # Prepare Questions
        # ---------------------------------

        available = []

        for index, q in enumerate(questions):

            question = q.copy()


            # Create id if missing

            if "id" not in question:

                question["id"] = index + 1


            available.append(question)



        self.validate_questions(
            available
        )



        structured = []


        question_no = 1



        # ---------------------------------
        # Create Question Blocks
        # ---------------------------------

        while len(available) >= 2:



            block = {


                "question_no": question_no,


                "parts": [],


                "or": None


            }



            # =====================
            # PART A
            # =====================


            part_a = available.pop(0)



            block["parts"].append({

                "label": "A",

                "question": part_a

            })




            # =====================
            # PART B
            # =====================


            part_b = available.pop(0)



            block["parts"].append({

                "label": "B",

                "question": part_b

            })




            # =====================
            # OR B
            # =====================


            alternative = self.find_alternative(

                part_b,

                available

            )



            if alternative:


                block["or"] = {


                    "label": "B",


                    "question": alternative


                }


                available.remove(

                    alternative

                )




            structured.append(block)



            question_no += 1




        return structured





    # =================================================
    # VALIDATION
    # =================================================


    def validate_questions(

            self,

            questions

    ):



        for index, q in enumerate(questions):


            required = [


                "id",

                "text",

                "marks"


            ]



            for field in required:



                if field not in q:



                    raise Exception(


                        f"Question {index+1} missing field: {field}"


                    )







    # =================================================
    # SCORING
    # =================================================


    def score(

            self,

            original,

            candidate

    ):


        score = 0



        # Same marks compulsory


        if candidate["marks"] != original["marks"]:


            return -1



        score += 100




        # Same CO preference


        if candidate.get("co") == original.get("co"):


            score += 30





        # Same Bloom Level


        if candidate.get("bl") == original.get("bl"):


            score += 25





        # Same difficulty


        if candidate.get("difficulty") == original.get("difficulty"):


            score += 20





        # Same Unit


        if candidate.get("unit") == original.get("unit"):


            score += 10




        return score





    # =================================================
    # FIND BEST OR QUESTION
    # =================================================


    def find_alternative(

            self,

            original,

            candidates

    ):


        best = None


        best_score = -1




        for q in candidates:



            if q["id"] == original["id"]:

                continue




            current_score = self.score(

                original,

                q

            )



            if current_score > best_score:



                best_score = current_score


                best = q




        return best