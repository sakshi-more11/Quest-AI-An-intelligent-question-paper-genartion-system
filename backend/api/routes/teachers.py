from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database.database import get_db

from backend.schemas.teacher import (
    TeacherCreate,
    TeacherUpdate,
    TeacherResponse,
)

from backend.api.services.teacher_service import teacher_service


router = APIRouter(
    prefix="/teachers",
    tags=["Teacher Management"]
)


# ---------------------------------------------------------
# Get All Teachers
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[TeacherResponse]
)
def get_teachers(
    db: Session = Depends(get_db)
):

    return teacher_service.get_all(db)


# ---------------------------------------------------------
# Get Single Teacher
# ---------------------------------------------------------

@router.get(
    "/{teacher_id}",
    response_model=TeacherResponse
)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = teacher_service.get(db, teacher_id)

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


# ---------------------------------------------------------
# Create Teacher
# ---------------------------------------------------------

@router.post(
    "",
    response_model=TeacherResponse
)
def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):

    return teacher_service.create(
        db,
        teacher
    )


# ---------------------------------------------------------
# Update Teacher
# ---------------------------------------------------------

@router.put(
    "/{teacher_id}",
    response_model=TeacherResponse
)
def update_teacher(
    teacher_id: int,
    teacher: TeacherUpdate,
    db: Session = Depends(get_db)
):

    updated = teacher_service.update(
        db,
        teacher_id,
        teacher
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return updated


# ---------------------------------------------------------
# Disable Teacher
# ---------------------------------------------------------

@router.patch(
    "/{teacher_id}/disable",
    response_model=TeacherResponse
)
def disable_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = teacher_service.disable(
        db,
        teacher_id
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


# ---------------------------------------------------------
# Enable Teacher
# ---------------------------------------------------------

@router.patch(
    "/{teacher_id}/enable",
    response_model=TeacherResponse
)
def enable_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = teacher_service.enable(
        db,
        teacher_id
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


# ---------------------------------------------------------
# Delete Teacher
# ---------------------------------------------------------

@router.delete(
    "/{teacher_id}"
)
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    deleted = teacher_service.delete(
        db,
        teacher_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return {
        "message": "Teacher deleted successfully"
    }