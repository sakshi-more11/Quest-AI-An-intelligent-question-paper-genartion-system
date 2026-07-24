from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

from backend.database.base import Base



class Template(Base):

    __tablename__ = "templates"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        nullable=False
    )


    template_name = Column(
        String,
        nullable=False
    )


    template_json = Column(
        JSON,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )