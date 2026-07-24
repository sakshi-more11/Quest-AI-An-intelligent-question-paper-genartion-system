from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.database.database import get_db

from backend.crud.crud_upload import get_uploads


router = APIRouter(
    prefix="/uploads",
    tags=["Upload Center"]
)


@router.get("/{teacher_id}")

def list_uploads(

    teacher_id: int,

    db: Session = Depends(get_db)

):

    return get_uploads(
        db,
        teacher_id
    )


@router.get("/templates/{teacher_id}")

def list_templates(

    teacher_id: int,

    db: Session = Depends(get_db)

):

    return get_templates(
        db,
        teacher_id
    )