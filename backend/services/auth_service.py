"""
Authentication Service
"""

from sqlalchemy.orm import Session

from backend.models.user import User

from backend.auth.password import (
    hash_password,
    verify_password
)


class AuthService:

    # -------------------------------------------------
    # Register User
    # -------------------------------------------------

    def register(

        self,

        db: Session,

        full_name: str,

        email: str,

        password: str,

        role: str

    ):

        existing_user = db.query(User).filter(

            User.email == email

        ).first()

        if existing_user:

            raise Exception(

                "Email already registered."

            )

        new_user = User(

            full_name=full_name,

            email=email,

            password=hash_password(password),   # ✅ FIXED

            role=role

        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return new_user

    # -------------------------------------------------
    # Login User
    # -------------------------------------------------

    def login(

        self,

        db: Session,

        email: str,

        password: str

    ):

        user = db.query(User).filter(

            User.email == email

        ).first()

        if user is None:

            return None

        if not verify_password(

            password,

            user.password      

        ):

            return None

        return user