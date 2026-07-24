from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from sqlalchemy.orm import relationship

from backend.database.base import Base


class Knowledge(Base):

    __tablename__ = "knowledge"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    file_id = Column(
        Integer,
        ForeignKey("uploaded_files.id"),
        nullable=False
    )

    # Extracted chunk text
    content = Column(
        String,
        nullable=False
    )

    # Reference to FAISS embedding
    embedding_id = Column(
        String,
        nullable=True
    )

    # Vector store name
    vector_store = Column(
        String,
        default="faiss"
    )

    # Chunk statistics
    total_chunks = Column(
        Integer,
        default=0
    )

    processed = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    file = relationship(
        "UploadedFile",
        back_populates="knowledge_records"
    )

    subject_id = Column(
    Integer,
    ForeignKey("subjects.id")
    )

    subject = relationship(
        "Subject",
        back_populates="knowledge_records"
    )