from sqlalchemy.orm import Session

from backend.models.user import User


class TeacherService:

    # --------------------------------------------------
    # Get all teachers
    # --------------------------------------------------

    def get_all(self, db: Session):

        return (
            db.query(User)
            .filter(User.role == "teacher")
            .order_by(User.full_name)
            .all()
        )

    # --------------------------------------------------
    # Get single teacher
    # --------------------------------------------------

    def get(self, db: Session, teacher_id: int):

        return (
            db.query(User)
            .filter(
                User.id == teacher_id,
                User.role == "teacher"
            )
            .first()
        )

    # --------------------------------------------------
    # Create teacher
    # --------------------------------------------------

    def create(self, db: Session, teacher):

        new_teacher = User(

            full_name=teacher.full_name,

            email=teacher.email,

            password=teacher.password,

            designation=teacher.designation,

            department=teacher.department,

            subject=teacher.subject,

            role="teacher",

            is_active=True

        )

        db.add(new_teacher)

        db.commit()

        db.refresh(new_teacher)

        return new_teacher

    # --------------------------------------------------
    # Update teacher
    # --------------------------------------------------

    def update(self, db: Session, teacher_id: int, teacher):

        db_teacher = self.get(db, teacher_id)

        if not db_teacher:
            return None

        db_teacher.full_name = teacher.full_name
        db_teacher.designation = teacher.designation
        db_teacher.department = teacher.department
        db_teacher.subject = teacher.subject

        db.commit()

        db.refresh(db_teacher)

        return db_teacher

    # --------------------------------------------------
    # Disable teacher
    # --------------------------------------------------

    def disable(self, db: Session, teacher_id: int):

        teacher = self.get(db, teacher_id)

        if not teacher:
            return None

        teacher.is_active = False

        db.commit()

        return teacher

    # --------------------------------------------------
    # Enable teacher
    # --------------------------------------------------

    def enable(self, db: Session, teacher_id: int):

        teacher = self.get(db, teacher_id)

        if not teacher:
            return None

        teacher.is_active = True

        db.commit()

        return teacher

    # --------------------------------------------------
    # Delete teacher
    # --------------------------------------------------

    def delete(self, db: Session, teacher_id: int):

        teacher = self.get(db, teacher_id)

        if not teacher:
            return False

        db.delete(teacher)

        db.commit()

        return True


teacher_service = TeacherService()