from dataclasses import dataclass
from typing import List


@dataclass
class Section:

    name: str

    marks_per_question: int

    number_of_questions: int

    compulsory: bool = True


@dataclass
class PaperBlueprint:

    subject: str

    exam_type: str

    total_marks: int

    sections: List[Section]

    bloom_distribution: dict

    difficulty_distribution: dict

    units: List[int]