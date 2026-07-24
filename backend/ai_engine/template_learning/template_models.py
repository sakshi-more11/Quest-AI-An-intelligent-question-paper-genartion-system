from dataclasses import dataclass, field


@dataclass
class QuestionTemplate:

    question_no: str

    sub_question: str

    marks: int

    has_choice: bool = False

    section: str = ""


@dataclass
class SectionTemplate:

    name: str

    questions: list = field(default_factory=list)


@dataclass
class PaperTemplate:

    total_marks: int

    sections: list = field(default_factory=list)