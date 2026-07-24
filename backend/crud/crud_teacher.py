from sqlalchemy.orm import Session

from backend.models.user import User

from backend.core.security import hash_password


def get_all_teachers(db: Session):

    return db.query(User).filter(
        User.role == "teacher"
    ).all()


def get_teacher(db: Session, teacher_id: int):

    return db.query(User).filter(
        User.id == teacher_id
    ).first()


def get_teacher_by_email(db: Session, email: str):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_teacher(db: Session, teacher):

    obj = User(

        full_name=teacher.full_name,

        email=teacher.email,

        password=hash_password(
            teacher.password
        ),

        designation=teacher.designation,

        department=teacher.department,

        subject=teacher.subject,

        role="teacher",

        is_active=True

    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj


def update_teacher(db, teacher, data):

    teacher.full_name = data.full_name
    teacher.designation = data.designation
    teacher.department = data.department
    teacher.subject = data.subject

    db.commit()

    db.refresh(teacher)

    return teacher


def disable_teacher(db, teacher):

    teacher.is_active = False

    db.commit()

    return teacher


def enable_teacher(db, teacher):

    teacher.is_active = True

    db.commit()

    return teacher


def delete_teacher(db, teacher):

    db.delete(teacher)

    db.commit()