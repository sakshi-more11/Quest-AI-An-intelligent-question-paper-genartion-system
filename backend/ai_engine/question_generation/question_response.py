from dataclasses import dataclass


@dataclass
class QuestionResponse:

    questions: list

    retrieved_chunks: list

    prompt: str

    model_used: str

    success: bool

    message: str