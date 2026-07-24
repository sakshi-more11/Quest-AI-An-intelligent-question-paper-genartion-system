from dataclasses import dataclass, field
from typing import List, Optional



@dataclass
class QuestionSchema:


    text: str

    marks: int

    unit: str

    co: str

    bl: str = ""

    difficulty: str = ""

    embedding: Optional[List[float]] = field(
        default=None
    )

    confidence: float = 0.0

    source: str = "Question Bank"

    question_type: str = "Theory"

    keywords: List[str] = field(
        default_factory=list
    )


    def to_dict(self):

        return {

            "text": self.text,

            "marks": self.marks,

            "unit": self.unit,

            "co": self.co,

            "bl": self.bl,

            "bloom": self.bl,

            "difficulty": self.difficulty,

            "embedding": self.embedding,

            "confidence": self.confidence,

            "source": self.source,

            "question_type": self.question_type,

            "keywords": self.keywords
        }