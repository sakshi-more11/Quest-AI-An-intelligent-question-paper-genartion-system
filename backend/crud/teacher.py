from sqlalchemy.orm import Session

from backend.models.user import User


def get_teachers(db: Session):
    return (
        db.query(User)
        .filter(User.role == "teacher")
        .all()
    )


def get_teacher(db: Session, teacher_id: int):
    return (
        db.query(User)
        .filter(User.id == teacher_id)
        .first()
    )


def create_teacher(db: Session, teacher):
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, teacher):
    db.delete(teacher)
    db.commit()


def update_teacher(db: Session, teacher):
    db.commit()
    db.refresh(teacher)
    return teacher