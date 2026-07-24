from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from sqlalchemy.orm import relationship

from backend.database.base import Base



class UploadedFile(Base):

    __tablename__ = "uploaded_files"



    id = Column(
        Integer,
        primary_key=True,
        index=True
    )



    filename = Column(
        String,
        nullable=False
    )



    filepath = Column(
        String,
        nullable=False
    )



    file_type = Column(
        String,
        nullable=True
    )



    # NEW
    upload_category = Column(
        String,
        nullable=False
    )


    # NEW
    subject_id = Column(
        Integer,
        ForeignKey(
            "subjects.id"
        ),
        nullable=False
    )



    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )



    user_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        )
    )



    # USER RELATION

    user = relationship(
        "User",
        back_populates="uploaded_files"
    )



    # SUBJECT RELATION

    subject = relationship(
        "Subject",
        back_populates="uploaded_files"
    )



    # KNOWLEDGE RELATION

    knowledge_records = relationship(
        "Knowledge",
        back_populates="file"
    )