"""
question.py

Schema for Question Generation Request
"""

from pydantic import BaseModel


class QuestionRequest(BaseModel):

    subject: str

    unit: str = "All"

    number_of_questions: int = 5

    marks: int = 10

    question_type: str = "Descriptive"

    difficulty: str = "Medium"

    bloom_level: str = "Apply"

    top_k_context: int = 5