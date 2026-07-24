from typing import List

from pydantic import BaseModel


class QuestionItem(BaseModel):

    question: str

    marks: int

    bloom_level: str

    unit: str

    difficulty: str = ""

    question_type: str = ""


class PaperGenerateRequest(BaseModel):

    title: str

    subject: str

    duration: str

    total_marks: int

    generated_question_pool: List[QuestionItem]


class PaperGenerateResponse(BaseModel):

    success: bool

    paper: dict

    validation: dict