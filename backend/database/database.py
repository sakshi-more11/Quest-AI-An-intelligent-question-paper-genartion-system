"""
database.py

Database configuration for QuestAI.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from backend.api.core.config import settings

# -------------------------------------------------
# Database URL
# -------------------------------------------------

DATABASE_URL = settings.DATABASE_URL

# -------------------------------------------------
# SQLAlchemy Engine
# -------------------------------------------------

engine = create_engine(

    DATABASE_URL,

    connect_args={"check_same_thread": False}

)

# -------------------------------------------------
# Session Factory
# -------------------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)
Base = declarative_base()
# -------------------------------------------------
# Dependency for FastAPI
# -------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()