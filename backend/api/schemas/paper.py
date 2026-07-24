"""
paper.py
"""

from pydantic import BaseModel, ConfigDict
from typing import Any, Optional


class PaperRequest(BaseModel):

    subject: str

    total_marks: int = 50

    marks_distribution: dict[int, int] = {2: 5, 5: 4, 10: 2}

    duration: str = "3 Hours"

    template: Optional[Any] = None
    questions: list[dict] = []
    syllabus: Optional[dict] = None

    model_config = ConfigDict(extra="allow")
