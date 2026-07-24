from dotenv import load_dotenv

import os

load_dotenv()


class Settings:

    OPENROUTER_API_KEY = os.getenv(
        "OPENROUTER_API_KEY"
    )

    OPENROUTER_MODEL = os.getenv(
        "OPENROUTER_MODEL"
    )

    PROJECT_NAME = "QuestAI"

    VERSION = "1.0.0"


settings = Settings()