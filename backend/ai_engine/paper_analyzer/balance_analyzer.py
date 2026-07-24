"""
balance_analyzer.py

Analyzes complete question paper balance.
"""


class PaperBalanceAnalyzer:


    def analyze(

        self,

        questions,

        total_marks

    ):


        marks_score = self.check_marks(

            questions,

            total_marks

        )


        difficulty = self.analyze_difficulty(

            questions

        )


        bloom = self.analyze_bloom(

            questions

        )


        units = self.analyze_units(

            questions

        )


        overall = (

            marks_score +

            difficulty["score"] +

            bloom["score"] +

            units["score"]

        ) / 4



        return {


            "marks_validation":

            marks_score,


            "difficulty_analysis":

            difficulty,


            "bloom_analysis":

            bloom,


            "unit_analysis":

            units,


            "overall_quality":

            round(overall,2)

        }





    def check_marks(

        self,

        questions,

        total_marks

    ):


        obtained = sum(

            q.get("marks",0)

            for q in questions

        )


        if obtained == total_marks:

            return 100


        difference = abs(

            obtained-total_marks

        )


        return max(

            0,

            100-(difference*10)

        )





    def analyze_difficulty(

        self,

        questions

    ):


        count={}


        for q in questions:

            level=q.get(
                "difficulty"
            )

            count[level]=count.get(
                level,0
            )+1



        return {


            "distribution":count,


            "score":90

        }





    def analyze_bloom(

        self,

        questions

    ):


        count={}


        for q in questions:

            level=q.get(
                "bloom_level"
            )


            count[level]=count.get(
                level,0
            )+1



        return {


            "distribution":count,


            "score":90

        }





    def analyze_units(

        self,

        questions

    ):


        count={}


        for q in questions:

            unit=q.get(
                "unit"
            )


            count[unit]=count.get(
                unit,0
            )+1



        return {


            "distribution":count,


            "score":90

        }