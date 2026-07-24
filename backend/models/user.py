from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from backend.database.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="teacher"
    )

    # ───────── Teacher Information ─────────

    designation = Column(
        String,
        default="Assistant Professor"
    )

    department = Column(
        String,
        default="AI & ML"
    )

    subject = Column(
        String,
        default=""
    )

    # True = Active
    # False = Disabled

    is_active = Column(
        Boolean,
        default=True
    )

    # ───────── Relationships ─────────

    uploaded_files = relationship(
        "UploadedFile",
        back_populates="user"
    )

    papers = relationship(
        "QuestionPaper",
        back_populates="creator"
    )

    history = relationship(
        "History",
        back_populates="user"
    )