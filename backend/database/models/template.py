from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

from backend.database.database import Base


class Template(Base):

    __tablename__="templates"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        nullable=True
    )


    template_name = Column(
        String,
        nullable=False
    )


    original_filename = Column(
        String,
        nullable=True
    )


    template_json = Column(
        JSON,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )