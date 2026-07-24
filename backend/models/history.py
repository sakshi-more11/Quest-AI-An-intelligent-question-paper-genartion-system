from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from sqlalchemy.orm import relationship

from backend.database.base import Base



class History(Base):

    __tablename__ = "history"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    action = Column(
        String,
        nullable=False
    )


    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )


    user = relationship(
        "User",
        back_populates="history"
    )