class PaperQualityAnalyzer:


    def __init__(self):

        from backend.ai_engine.quality_analyzer.bloom_validator import BloomValidator
        from backend.ai_engine.quality_analyzer.difficulty_validator import DifficultyValidator
        from backend.ai_engine.quality_analyzer.coverage_validator import CoverageValidator


        self.bloom = BloomValidator()

        self.difficulty = DifficultyValidator()

        self.coverage = CoverageValidator()



    def analyze(self, paper):


        report = {}


        report["bloom_analysis"] = self.bloom.check(
            paper
        )


        report["difficulty_analysis"] = self.difficulty.check(
            paper
        )


        report["coverage_analysis"] = self.coverage.check(
            paper
        )


        report["overall_score"] = self.calculate_score(
            report
        )


        return report



    def calculate_score(self, report):


        score = 100


        for key,value in report.items():

            if isinstance(value,dict):

                if value.get("status")=="warning":

                    score -= 10


        return max(score,0)