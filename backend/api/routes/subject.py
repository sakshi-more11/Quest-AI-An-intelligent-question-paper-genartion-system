from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database.dependency import get_db
from backend.api.dependencies.auth import get_current_user

from backend.models.subject import Subject

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)


@router.get("/")
def get_subjects(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    subjects = db.query(Subject).all()

    return subjects


@router.post("/")
def create_subject(

    payload: dict,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    existing = db.query(Subject).filter(

        Subject.code == payload["code"]

    ).first()

    if existing:

        raise HTTPException(

            status_code=400,

            detail="Subject already exists"

        )

    subject = Subject(

        name=payload["name"],

        code=payload["code"],

        description=payload.get("description", "")

    )

    db.add(subject)

    db.commit()

    db.refresh(subject)

    return subject