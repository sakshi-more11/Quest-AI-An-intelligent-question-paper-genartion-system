from sqlalchemy.orm import Session

from backend.models.user import User
from backend.auth.password import hash_password



class AdminService:


    def create_teacher(
        self,
        db: Session,
        data
    ):

        existing = db.query(User).filter(
            User.email == data.email
        ).first()


        if existing:
            raise Exception(
                "Email already exists"
            )


        teacher = User(

            full_name=data.full_name,

            email=data.email,

            password=hash_password(
                data.password
            ),

            role="teacher",

            is_active=True
        )


        db.add(teacher)

        db.commit()

        db.refresh(teacher)


        return teacher



    def get_teachers(
        self,
        db:Session
    ):

        return db.query(User).filter(
            User.role=="teacher"
        ).all()



    def disable_teacher(
        self,
        db:Session,
        teacher_id:int
    ):

        teacher=db.query(User).filter(
            User.id==teacher_id
        ).first()


        if teacher:

            teacher.is_active=False

            db.commit()


        return teacher



    def enable_teacher(
        self,
        db:Session,
        teacher_id:int
    ):


        teacher=db.query(User).filter(
            User.id==teacher_id
        ).first()


        if teacher:

            teacher.is_active=True

            db.commit()


        return teacher



    def delete_teacher(
        self,
        db:Session,
        teacher_id:int
    ):


        teacher=db.query(User).filter(
            User.id==teacher_id
        ).first()


        if teacher:

            db.delete(teacher)

            db.commit()


        return True



admin_service = AdminService()