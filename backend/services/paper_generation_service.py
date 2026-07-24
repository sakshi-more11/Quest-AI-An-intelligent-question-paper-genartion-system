"""
QuestAI Paper Generation Service

Step 10 Complete

Pipeline:

Template Fetch
        |
Template Normalization + Validation
        |
Question Intelligence Engine
        |
OR Generation
        |
Paper Structure
        |
Quality Validation
        |
PDF Rendering
        |
Final Validation
        |
Response
"""


import copy
import os



from backend.services.template_service import TemplateService


from backend.ai.question_selection.question_selector import (
    QuestionSelector
)

from backend.ai_engine.intelligence_pipeline.question_intelligence import (
    QuestionIntelligence
)
from backend.ai.template_engine.pdf_template_renderer import (
    PDFTemplateRenderer
)


from backend.ai.template_engine.template_validator import (
    TemplateValidator
)


from backend.ai.quality_assurance.paper_quality_checker import (
    PaperQualityChecker
)


from backend.ai.generation.or_question_generator import (
    ORQuestionGenerator
)


from backend.ai.generation.paper_structure_generator import (
    PaperStructureGenerator
)





class PaperGenerationService:



    def __init__(self):


        self.template_service = TemplateService()


        self.renderer = PDFTemplateRenderer()


        self.quality_checker = PaperQualityChecker()


        self.or_generator = ORQuestionGenerator()


        self.structure_generator = PaperStructureGenerator()


        self.template_validator = TemplateValidator()


        # Block 4
        self.question_selector = QuestionSelector()

        self.question_intelligence = QuestionIntelligence()



    def generate(

        self,

        template_id,

        metadata,

        questions

    ):


        print("========================")
        print("QUESTIONS RECEIVED")
        print("========================")


        for q in questions:

            print(q)





        # =====================================
        # 1 TEMPLATE FETCH
        # =====================================


        template = self.template_service.get_template(
            template_id
        )



        if not template:

            raise Exception(
                "Template not found"
            )





        # =====================================
        # 2 TEMPLATE NORMALIZATION
        # =====================================


        raw_template = copy.deepcopy(
            template.template_json
        )



        print("========================")
        print("RAW TEMPLATE")
        print("========================")

        print(raw_template)



        template_json = self.template_validator.prepare(
            raw_template
        )



        print("========================")
        print("NORMALIZED TEMPLATE")
        print("========================")

        print(template_json)




        template_report = {


            "valid":True,


            "message":
            "Template validated and normalized successfully"


        }

        # =====================================
        # 3 QUESTION SELECTION
        # =====================================

        selection_result = self.question_selector.select(

            questions,

            count=len(questions),

            total_marks=sum(

                q.get("marks", 0)

                for q in questions

            )

        )

        questions = selection_result["questions"]

        print("========================")
        print("QUESTION SELECTION REPORT")
        print("========================")

        print(selection_result["validation"])


        # =====================================
        # 4 QUESTION INTELLIGENCE
        # =====================================

        print("========================")
        print("QUESTION INTELLIGENCE")
        print("========================")

        questions = self.question_intelligence.analyze_questions(
            questions
        )

        print("========================")
        print("AFTER QUESTION INTELLIGENCE")
        print("========================")

        for q in questions:
            print(q)

        # =====================================
        # 5 OR GENERATION
        # =====================================


        formatted_questions = self.or_generator.generate(

            questions

        )

        print("========================")
        print("AFTER OR GENERATOR")
        print("========================")

        print(formatted_questions)



        # =====================================
        # 6 PAPER STRUCTURE
        # =====================================


        paper_structure = self.structure_generator.generate(

            formatted_questions,

            template_json

        )

        print("========================")
        print("PAPER STRUCTURE")
        print("========================")

        from pprint import pprint
        pprint(paper_structure)

        print("========================")
        print("PAPER STRUCTURE GENERATED")
        print("========================")





        # =====================================
        # 7 INJECT DATA
        # =====================================


        template_json["metadata"] = metadata


        template_json["questions"] = paper_structure





        # =====================================
        # 8 QUALITY CHECK
        # =====================================


        estimated_pages = self.calculate_pages(

            paper_structure

        )




        quality_report = self.quality_checker.validate(

            template_json,

            metadata,

            paper_structure,

            pages=estimated_pages

        )



        print("========================")
        print("QUALITY REPORT")
        print("========================")

        print(quality_report)





        if quality_report["status"]=="FAILED":

            raise Exception({

                "stage":
                "Quality Validation",

                "report":
                quality_report

            })





        # =====================================
        # 9 PDF GENERATION
        # =====================================


        output_directory="storage/output"


        os.makedirs(

            output_directory,

            exist_ok=True

        )



        course_code = metadata.get(

            "course_code",

            "generated"

        )



        output_path=os.path.join(

            output_directory,

            f"{course_code}_question_paper.pdf"

        )





        generated_file=self.renderer.render(

            template_json,

            metadata,

            paper_structure,

            output_path

        )



        print("========================")
        print("PDF GENERATED")
        print(generated_file)
        print("========================")

        print("========================")
        print("AI REPOSITORY")
        print("========================")

        print(

            self.question_intelligence.report()

        )


        # =====================================
        # 10 FINAL CHECK
        # =====================================


        final_report=self.final_file_check(

            generated_file

        )
        if not final_report["valid"]:

            raise Exception({

                "stage": "Final PDF Validation",

                "report": final_report

            })


        print(final_report)





        return {


            "success":True,


            "file":generated_file,


            "pages":estimated_pages,


            "template_validation":template_report,


            "quality":quality_report,


            "final_check":final_report,
            "intelligence": self.question_intelligence.report()

        }







    def calculate_pages(

        self,

        paper_structure

    ):


        count=0



        for section in paper_structure:

            count+=len(

                section.get(

                    "questions",

                    []

                )

            )



        if count<=4:

            return 1


        elif count<=8:

            return 2


        return 3






    def final_file_check(

        self,

        file_path

    ):


        if not os.path.exists(file_path):

            return {

                "valid":False,

                "message":"PDF not generated"

            }




        size=os.path.getsize(file_path)



        if size<1000:

            return {

                "valid":False,

                "message":"Generated PDF empty"

            }



        return {


            "valid":True,


            "message":"PDF generated successfully"


        }