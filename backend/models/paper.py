from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from sqlalchemy.orm import relationship

from backend.database.base import Base



class QuestionPaper(Base):

    __tablename__ = "question_papers"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=True
    )


    total_marks = Column(
        Integer,
        nullable=False
    )


    paper_json = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    subject_id = Column(
        Integer,
        ForeignKey("subjects.id")
    )


    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )


    subject = relationship(
        "Subject",
        back_populates="papers"
    )


    creator = relationship(
        "User",
        back_populates="papers"
    )