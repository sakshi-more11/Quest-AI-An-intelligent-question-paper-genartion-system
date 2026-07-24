from pydantic import BaseModel
from typing import List


class QuestionModel(BaseModel):

    question: str

    marks: int

    difficulty: str

    bloom_level: str

    unit: str

    question_type: str


class GenerateQuestionResponse(BaseModel):

    success: bool

    message: str

    model: str

    questions: List[QuestionModel]