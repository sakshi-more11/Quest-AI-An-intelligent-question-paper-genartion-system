class BloomValidator:


    def check(self,paper):


        levels=[]


        for section in paper["sections"]:

            for q in section["questions"]:

                levels.append(
                    q.get("bloom_level")
                )


        unique=set(levels)


        if len(unique)>=2:

            status="good"

        else:

            status="warning"


        return {

            "status":status,

            "levels_found":list(unique),

            "message":
            "Bloom taxonomy distribution checked"

        }