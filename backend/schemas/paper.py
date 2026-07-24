from pydantic import BaseModel
from typing import List, Optional


class PaperRequest(BaseModel):

    subject: str

    duration: str = "3 Hours"

    total_marks: int

    number_of_questions: int = 3

    difficulty: Optional[str] = "Medium"

    bloom_level: Optional[str] = None
