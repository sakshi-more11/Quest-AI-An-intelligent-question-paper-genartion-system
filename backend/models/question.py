from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from sqlalchemy.orm import relationship

from backend.database.base import Base


class Question(Base):

    __tablename__ = "questions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # -----------------------------
    # Question Content
    # -----------------------------

    question_text = Column(
        String,
        nullable=False
    )


    # -----------------------------
    # Unit / Chapter
    # -----------------------------

    unit = Column(
        String,
        nullable=True
    )


    # -----------------------------
    # Marks
    # -----------------------------

    marks = Column(
        Integer,
        default=5
    )


    # -----------------------------
    # Bloom Taxonomy
    # BT1 - BT6
    # -----------------------------

    blooms_level = Column(
        String,
        nullable=True
    )


    # -----------------------------
    # Difficulty
    # Easy Medium Hard
    # -----------------------------

    difficulty = Column(
        String,
        nullable=True
    )


    # -----------------------------
    # Question Type
    # Theory / Numerical / Design
    # -----------------------------

    question_type = Column(
        String,
        nullable=True
    )


    # -----------------------------
    # Expected Answer Points
    # -----------------------------

    expected_answer_points = Column(
        String,
        nullable=True
    )


    # -----------------------------
    # CO Mapping
    # Phase 12
    # -----------------------------

    # Course Outcome Mapping

    co_mapping = Column(

        String,

        nullable=True

    )


    # -----------------------------
    # Source Document
    # syllabus/material/PYQ
    # -----------------------------

    source_file_id = Column(
        Integer,
        ForeignKey(
            "uploaded_files.id"
        ),
        nullable=True
    )


    # -----------------------------
    # AI Generated Flag
    # -----------------------------

    ai_generated = Column(
        Boolean,
        default=True
    )


    # -----------------------------
    # Subject Relation
    # -----------------------------

    subject_id = Column(
        Integer,
        ForeignKey(
            "subjects.id"
        ),
        nullable=False
    )


    subject = relationship(
        "Subject",
        back_populates="questions"
    )


    # -----------------------------
    # Created Time
    # -----------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )