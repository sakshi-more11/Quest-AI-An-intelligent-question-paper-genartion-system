from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from sqlalchemy.orm import relationship

from backend.database.base import Base


class Subject(Base):

    __tablename__ = "subjects"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    code = Column(
        String,
        nullable=True
    )


    description = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    questions = relationship(
        "Question",
        back_populates="subject"
    )


    papers = relationship(
        "QuestionPaper",
        back_populates="subject"
    )


    uploaded_files = relationship(
        "UploadedFile",
        back_populates="subject"
    )


    # Knowledge chunks generated from study material
    knowledge_records = relationship(
        "Knowledge",
        back_populates="subject"
    )