"""
report_generator.py

Creates readable paper analysis report.
"""


class AnalysisReport:


    def generate(

        self,

        analysis

    ):


        print("\n")
        print("="*50)

        print("QUESTAI PAPER QUALITY REPORT")

        print("="*50)



        print(
            "Marks Score:",
            analysis["marks_validation"]
        )


        print(
            "Difficulty:",
            analysis["difficulty_analysis"]
        )


        print(
            "Bloom:",
            analysis["bloom_analysis"]
        )


        print(
            "Units:",
            analysis["unit_analysis"]
        )


        print(
            "Overall Quality:",
            analysis["overall_quality"]
        )