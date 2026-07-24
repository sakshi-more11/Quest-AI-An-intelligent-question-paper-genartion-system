class CoverageValidator:


    def check(self,paper):


        units=[]


        for section in paper["sections"]:

            for q in section["questions"]:

                units.append(
                    q.get("unit")
                )


        return {

            "status":"good",

            "units_covered":
            list(set(units))

        }