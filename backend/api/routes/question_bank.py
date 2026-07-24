from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session


from backend.database.dependency import get_db

from backend.api.dependencies.auth import get_current_user


from backend.models.question import Question

from backend.models.subject import Subject



router = APIRouter(

    prefix="/question-bank",

    tags=["Question Bank"]

)



# -------------------------------------------------
# Get Generated Question Bank
# -------------------------------------------------

@router.get("/{subject_id}")
def get_question_bank(

    subject_id: int,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)

):
    


    # -----------------------------------------
    # Validate Subject
    # -----------------------------------------

    subject = db.query(

        Subject

    ).filter(

        Subject.id == subject_id

    ).first()



    if subject is None:


        raise HTTPException(

            status_code=404,

            detail="Subject not found"

        )



    # -----------------------------------------
    # Fetch Questions
    # -----------------------------------------

    questions = db.query(

        Question

    ).filter(

        Question.subject_id == subject_id

    ).all()





    return {


        "subject":{


            "id": subject.id,


            "name": subject.name,


            "code": subject.code

        },



        "total_questions": len(questions),



        "questions":[



            {


                "id": q.id,


                "question": q.question_text,


                "marks": q.marks,


                "difficulty": q.difficulty,


                "blooms_level": q.blooms_level,


                "unit": q.unit,


                "question_type": q.question_type,


                "expected_answer_points":
                    q.expected_answer_points,


                "ai_generated":
                    q.ai_generated


            }


            for q in questions


        ]

    }

from backend.api.services.question_bank_service import question_bank_service


# -------------------------------------------------
# Generate Question Bank
# -------------------------------------------------

@router.post("/generate/{subject_id}")
def generate_question_bank(

    subject_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    subject = db.query(

        Subject

    ).filter(

        Subject.id == subject_id

    ).first()

    if subject is None:

        raise HTTPException(

            status_code=404,

            detail="Subject not found"

        )

    try:
        result = question_bank_service.generate(subject_id=subject_id, db=db)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        # Provider failures should be actionable to the UI, not an uncaught
        # traceback that fetch reports only as a generic network failure.
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return result
