from dataclasses import dataclass


@dataclass
class QuestionRequest:

    subject: str

    unit: str

    bloom_level: str

    difficulty: str

    marks: int

    question_type: str

    number_of_questions: int = 1

    top_k_context: int = 5