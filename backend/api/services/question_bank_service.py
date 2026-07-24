"""
question_bank_service.py

Question Bank Service
"""

from backend.models.question import Question
from backend.models.subject import Subject
from backend.models.uploaded_file import UploadedFile

from backend.ai_engine.question_bank.retriever import QuestionRetriever
from backend.ai_engine.question_bank.question_bank_builder import QuestionBankBuilder

from backend.api.services.knowledge_service import knowledge_service
from backend.ai_engine.paper_generation.analytics import build_analytics


class QuestionBankService:

    def __init__(self):

        self.builder = QuestionBankBuilder()

    # ---------------------------------------------------
    # Generate Question Bank
    # ---------------------------------------------------

    def generate(self, subject_id, db):

        # -----------------------------------------
        # Validate Subject
        # -----------------------------------------
        print("Generating questions using OpenRouter...")
        subject = (
            db.query(Subject)
            .filter(Subject.id == subject_id)
            .first()
        )

        if subject is None:
            raise ValueError("Subject not found.")

        categories = {
            row[0] for row in db.query(UploadedFile.upload_category).filter(
                UploadedFile.subject_id == subject_id
            ).all()
        }
        missing = {"syllabus", "material"} - categories
        if missing:
            raise ValueError(
                "Question-bank generation requires the subject syllabus and at least one study-material file. "
                "Missing: " + ", ".join(sorted(missing)) + "."
            )

        # -----------------------------------------
        # Load/Rebuild Knowledge Base
        # -----------------------------------------

        knowledge = knowledge_service.get()

        if (
            knowledge is None
            or knowledge.get("metadata", {}).get("subject_id") != subject_id
        ):

            knowledge = knowledge_service.build_subject_knowledge(
                subject_id,
                db
            )

        # -----------------------------------------
        # FAISS Retrieval
        # -----------------------------------------

        faiss_manager = knowledge["faiss"]


        print("==============================")
        print("DEBUG QUESTION BANK")
        print(
            "FAISS TOTAL:",
            faiss_manager.index.ntotal
        )

        print(
            "FAISS RECORDS:",
            len(faiss_manager.records)
        )


        retriever = QuestionRetriever(
            faiss_manager
        )


        chunks = retriever.retrieve(
            top_k=20
        )


        print(
            "RETRIEVED CHUNKS:",
            len(chunks)
        )

        print("==============================")

        if not chunks:
            raise ValueError(
                "No study material found for this subject."
            )

        # -----------------------------------------
        # Generate questions using OpenRouter
        # -----------------------------------------
        print("Chunks Retrieved:", len(chunks))

        for c in chunks[:3]:
            print(c[:200])
        questions = self.builder.generate(chunks)

        # -----------------------------------------
        # Remove Old AI Questions
        # -----------------------------------------

        db.query(Question).filter(
            Question.subject_id == subject_id
        ).delete()

        saved_questions = []

        # -----------------------------------------
        # Save New Questions
        # -----------------------------------------

        for q in questions:

            question = Question(

                subject_id=subject_id,

                question_text=q["question"],

                unit=q.get("unit", "Unit"),

                marks=int(q.get("marks", 5)),

                blooms_level=q.get(
                    "bloom_level",
                    "BT2"
                ),

                difficulty=q.get(
                    "difficulty",
                    "Medium"
                ),

                question_type="Descriptive",

                expected_answer_points="",

                ai_generated=True

            )

            db.add(question)

            saved_questions.append(question)

        db.commit()

        # -----------------------------------------
        # Refresh IDs
        # -----------------------------------------

        for q in saved_questions:
            db.refresh(q)
        chunks = retriever.retrieve(top_k=20)

        print("Retrieved chunks:", len(chunks))
        # -----------------------------------------
        # Return to Frontend
        # -----------------------------------------

        analytics = build_analytics(questions)
        quality = {
            "duplicatePreventionScore": round(100 - analytics["duplicate_percent"], 2),
            "syllabusCoverageScore": analytics["syllabus_coverage_percent"],
            "semanticAlignmentScore": round(100 - analytics["similarity_score"] / 4, 2),
            "overallAccuracy": round((100 - analytics["duplicate_percent"] + analytics["syllabus_coverage_percent"] + (100 - analytics["similarity_score"] / 4)) / 3, 2),
            "analytics": analytics,
        }

        return {

            "success": True,

            "count": len(saved_questions),

            "message": "Question Bank Generated Successfully",

            "quality": quality,

            "subject": {

                "id": subject.id,

                "name": subject.name,

                "code": subject.code

            },

            "questions": [

                {

                    "id": q.id,

                    "question_text": q.question_text,

                    "unit": q.unit,

                    "marks": q.marks,

                    "difficulty": q.difficulty,

                    "blooms_level": q.blooms_level,

                    "ai_generated": q.ai_generated

                }

                for q in saved_questions

            ]

        }
        

question_bank_service = QuestionBankService()
