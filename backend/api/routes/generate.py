"""
generate.py

Question Generation API
"""

from fastapi import APIRouter, Depends

from backend.api.dependencies.roles import require_teacher

from backend.api.schemas.question import QuestionRequest

from backend.api.services.generation_service import generation_service

from backend.database.database import SessionLocal

from backend.models.question import Question
from backend.models.subject import Subject


router = APIRouter(
    prefix="/generate",
    tags=["Question Generation"]
)


# -------------------------------------------------
# Generate Questions + Save to Database
# -------------------------------------------------

@router.post("/")
def generate_questions(

    request: QuestionRequest,

    current_user=Depends(require_teacher)

):

    # Generate using AI pipeline
    result = generation_service.generate(request)


    db = SessionLocal()

    saved_count = 0


    try:

        questions = result.questions
        subject = db.query(Subject).filter(Subject.name == request.subject).first()


        for q in questions:


            # if q is pydantic object
            if hasattr(q, "dict"):

                q = q.dict()


            if subject is None:
                continue

            question = Question(

                question_text=q.get(
                    "question",
                    ""
                ),

                marks=q.get(
                    "marks",
                    request.marks
                ),

                blooms_level=q.get(
                    "bloom_level",
                    request.bloom_level
                ),

                unit=q.get(
                    "unit",
                    request.unit
                ),
                difficulty=q.get("difficulty", request.difficulty),
                question_type=q.get("question_type", request.question_type),
                co_mapping=q.get("co"),
                subject_id=subject.id

            )


            db.add(question)

            saved_count += 1


        db.commit()


    except Exception as e:

        db.rollback()

        raise e


    finally:

        db.close()



    return {

        "success": True,

        "generated_by": current_user["email"],

        "role": current_user["role"],

        "saved_questions": saved_count,

        "result": result.__dict__,
        "warning": None if subject else "Questions were generated but not persisted: subject was not found."

    }



# -------------------------------------------------
# Health Check
# -------------------------------------------------

@router.get("/health")
def health():

    return {

        "module": "Question Generation",

        "status": "Ready"

    }
