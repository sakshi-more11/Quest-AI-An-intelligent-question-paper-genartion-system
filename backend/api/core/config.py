"""
Application Configuration
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    # -------------------------------------------------
    # Application
    # -------------------------------------------------

    APP_NAME = "QuestAI Backend"

    VERSION = "1.0.0"

    DEBUG = True

    API_PREFIX = "/api"

    # -------------------------------------------------
    # Gemini
    # -------------------------------------------------
    OPENROUTER_API_KEY: str

    OPENROUTER_MODEL: str = "openrouter/free"
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # -------------------------------------------------
    # JWT Authentication
    # -------------------------------------------------

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "questai_super_secret_key_change_in_production"
    )

    JWT_ALGORITHM = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(

        os.getenv(

            "ACCESS_TOKEN_EXPIRE_MINUTES",

            "60"

        )

    )

    # -------------------------------------------------
    # File Upload
    # -------------------------------------------------

    MAX_UPLOAD_SIZE = 20 * 1024 * 1024

    UPLOAD_FOLDER = "backend/uploads"

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    EXPORT_FOLDER = "exports"

    # -------------------------------------------------
    # Database
    # -------------------------------------------------

    DATABASE_URL = os.getenv(

        "DATABASE_URL",

        "sqlite:///./questai.db"

    )


settings = Settings()
