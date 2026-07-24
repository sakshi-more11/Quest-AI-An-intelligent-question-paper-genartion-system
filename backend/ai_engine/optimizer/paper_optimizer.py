"""
paper_optimizer.py

Complete QuestAI Intelligence Pipeline.
"""


from backend.ai_engine.paper_optimizer.constraint_selector import ConstraintSelector

from backend.ai_engine.paper_generation.multi_set_generator import MultiSetGenerator

from backend.ai_engine.quality_evaluator.question_quality_evaluator import QuestionQualityEvaluator

from backend.ai_engine.paper_analyzer.balance_analyzer import PaperBalanceAnalyzer




class PaperOptimizer:


    def __init__(

        self,

        rules

    ):


        self.selector = ConstraintSelector(
            rules
        )


        self.multi_generator = MultiSetGenerator(
            rules
        )


        self.evaluator = QuestionQualityEvaluator()


        self.analyzer = PaperBalanceAnalyzer()




    def optimize(

        self,

        questions,

        context,

        number_of_sets,

        questions_per_set,

        total_marks

    ):


        # --------------------------------
        # Step 1 : Generate Paper Sets
        # --------------------------------


        papers = self.multi_generator.generate_sets(

            questions,

            number_of_sets,

            questions_per_set

        )



        final_papers=[]



        for paper in papers:



            evaluated_questions=[]



            # --------------------------------
            # Step 2 : Quality Evaluation
            # --------------------------------


            for q in paper["questions"]:


                evaluation = self.evaluator.evaluate(

                    q["question"],

                    context,

                    q.get("bloom_level"),

                    q.get("difficulty")

                )


                q["quality_score"] = evaluation[
                    "overall_score"
                ]


                evaluated_questions.append(q)




            # --------------------------------
            # Step 3 : Paper Analysis
            # --------------------------------


            analysis = self.analyzer.analyze(

                evaluated_questions,

                total_marks

            )



            final_papers.append({


                "set_name":

                paper["set_name"],


                "questions":

                evaluated_questions,


                "analysis":

                analysis

            })



        return final_papers