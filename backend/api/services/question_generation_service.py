"""
QuestAI Question Generation Service

Phase 9.2

Flow:

Subject
   |
   |
Knowledge Table
   |
   |
OpenRouter
   |
   |
Quality Layer
   |
   |
Question Storage
"""


from backend.ai_engine.llm.llm_client import (
    LLMClient
)


from backend.ai_engine.prompts.question_prompt import (
    QuestionPromptBuilder
)


from backend.api.services.question_storage_service import (
    question_storage_service
)


# -----------------------------------------
# Quality Layer
# -----------------------------------------

from backend.ai_engine.quality.duplicate_detector import (
    DuplicateDetector
)


from backend.ai_engine.quality.difficulty_validator import (
    DifficultyValidator
)


from backend.models.uploaded_file import UploadedFile

from backend.models.knowledge import Knowledge

from backend.ai_engine.quality.bloom_mapper import (
    BloomMapper
)



class QuestionGenerationService:



    def __init__(self):


        self.llm = LLMClient()


        self.prompt_builder = QuestionPromptBuilder()



        # ---------------------------------
        # Quality Components
        # ---------------------------------

        self.duplicate_detector = DuplicateDetector()


        self.difficulty_validator = DifficultyValidator()
        self.bloom_mapper = BloomMapper()




    # -----------------------------------------
    # Generate Question Bank
    # -----------------------------------------

    def generate(

        self,

        subject_name,

        subject_id,

        db

    ):



        # -------------------------------------
        # Fetch uploaded files of subject
        # -------------------------------------

        files = db.query(

            UploadedFile

        ).filter(

            UploadedFile.subject_id == subject_id

        ).all()



        if not files:


            raise Exception(

                "No uploaded files found for subject"

            )




        file_ids = [

            file.id

            for file in files

        ]





        # -------------------------------------
        # Fetch Knowledge Chunks
        # -------------------------------------

        knowledge_records = db.query(

            Knowledge

        ).filter(

            Knowledge.file_id.in_(file_ids)

        ).all()




        if not knowledge_records:


            raise Exception(

                "Knowledge Base not built for subject"

            )





        chunks = []




        for record in knowledge_records:



            if record.content:


                chunks.append(

                    record.content

                )






        context = "\n\n".join(

            chunks

        )






        # -------------------------------------
        # Build Engineering Prompt
        # -------------------------------------

        prompt = self.prompt_builder.build(

            subject_name,

            context,

            number_of_questions=20

        )







        # -------------------------------------
        # OpenRouter generation
        # -------------------------------------

        questions = self.llm.generate_json(

            prompt

        )






        if not isinstance(

            questions,

            list

        ):


            raise Exception(

                "Invalid OpenRouter response format"

            )







        # -------------------------------------
        # QUALITY LAYER
        # -------------------------------------



        # Remove duplicate questions

        questions = self.duplicate_detector.remove_duplicates(

            questions

        )





        # Validate difficulty level

        questions = self.difficulty_validator.filter_questions(

            questions

        )



        # -------------------------------------
        # Bloom Taxonomy Mapping
        # -------------------------------------

        questions = self.bloom_mapper.map_questions(

            questions

        )




        # -------------------------------------
        # Add Default Metadata
        # -------------------------------------


        for question in questions:



            if "blooms_level" not in question:


                question["blooms_level"] = "BT4"





            if "unit" not in question:


                question["unit"] = "Auto"





            if "marks" not in question:


                question["marks"] = 10






        # -------------------------------------
        # Save Questions
        # -------------------------------------

        saved_questions = (

            question_storage_service.save_questions(

                questions,

                subject_id,

                db

            )

        )






        return {


            "generated":

            len(saved_questions),



            "questions":

            questions

        }







question_generation_service = (

    QuestionGenerationService()

)
