from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from backend.database.base import Base


class Material(Base):

    __tablename__ = "materials"

    id = Column(Integer, primary_key=True)

    filename = Column(String)

    original_name = Column(String)

    file_type = Column(String)

    subject = Column(String)

    uploaded_by = Column(Integer, ForeignKey("users.id"))

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    path = Column(String)