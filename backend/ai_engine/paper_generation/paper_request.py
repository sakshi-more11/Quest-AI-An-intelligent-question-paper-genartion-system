"""
paper_request.py

Request model for paper generation.
"""


class PaperRequest:


    def __init__(

        self,

        subject,

        total_marks,

        marks_distribution,

        generated_question_pool,

        template=None,

        duration="3 Hours"

    ):


        self.subject = subject

        self.total_marks = total_marks

        self.marks_distribution = marks_distribution

        self.generated_question_pool = generated_question_pool

        self.template = template

        self.duration = duration