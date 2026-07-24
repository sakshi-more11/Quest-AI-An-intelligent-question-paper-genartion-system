class DifficultyValidator:


    def check(self,paper):


        difficulty=[]


        for section in paper["sections"]:

            for q in section["questions"]:

                difficulty.append(
                    q.get("difficulty","Medium")
                )


        return {

            "status":"good",

            "distribution":{

                d:difficulty.count(d)

                for d in set(difficulty)

            }

        }