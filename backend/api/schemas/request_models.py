from pydantic import BaseModel


class GenerateQuestionRequest(BaseModel):

    subject: str

    unit: str

    bloom_level: str

    difficulty: str

    marks: int

    question_type: str

    number_of_questions: int = 5

    top_k_context: int = 5