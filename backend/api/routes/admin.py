from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from backend.api.dependencies.auth import admin_required
from backend.database.database import get_db

from backend.schemas.teacher_schema import (
    TeacherCreate,
    TeacherUpdate,
    TeacherResponse
)

from backend.crud.crud_teacher import (
    get_all_teachers,
    get_teacher,
    get_teacher_by_email,
    create_teacher,
    update_teacher,
    delete_teacher,
    disable_teacher,
    enable_teacher
)

#router = APIRouter(prefix="/admin",tags=["Teacher Management"])
router = APIRouter(
    prefix="/admin",
    tags=["Teacher Management"],
    dependencies=[Depends(admin_required)]
)

# --------------------------------------------------
# GET ALL TEACHERS
# --------------------------------------------------

@router.get(
    "/teachers",
    response_model=list[TeacherResponse]
)
def list_teachers(
    db: Session = Depends(get_db)
):

    return get_all_teachers(db)


# --------------------------------------------------
# CREATE TEACHER
# --------------------------------------------------

@router.post(
    "/teachers",
    response_model=TeacherResponse
)
def add_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):

    existing = get_teacher_by_email(
        db,
        teacher.email
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    return create_teacher(
        db,
        teacher
    )


# --------------------------------------------------
# UPDATE TEACHER
# --------------------------------------------------

@router.put(
    "/teachers/{teacher_id}",
    response_model=TeacherResponse
)
def edit_teacher(
    teacher_id: int,
    data: TeacherUpdate,
    db: Session = Depends(get_db)
):

    teacher = get_teacher(
        db,
        teacher_id
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found."
        )

    return update_teacher(
        db,
        teacher,
        data
    )


# --------------------------------------------------
# DISABLE
# --------------------------------------------------

@router.patch(
    "/teachers/{teacher_id}/disable",
    response_model=TeacherResponse
)
def disable(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = get_teacher(
        db,
        teacher_id
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found."
        )

    return disable_teacher(
        db,
        teacher
    )


# --------------------------------------------------
# ENABLE
# --------------------------------------------------

@router.patch(
    "/teachers/{teacher_id}/enable",
    response_model=TeacherResponse
)
def enable(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = get_teacher(
        db,
        teacher_id
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found."
        )

    return enable_teacher(
        db,
        teacher
    )


# --------------------------------------------------
# DELETE
# --------------------------------------------------

@router.delete(
    "/teachers/{teacher_id}"
)
def remove_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = get_teacher(
        db,
        teacher_id
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found."
        )

    delete_teacher(
        db,
        teacher
    )

    return {
        "message": "Teacher deleted successfully."
    }