"""
paper_builder.py

Builds final question paper.
"""


class PaperBuilder:


    def build(

        self,

        subject,

        sections,

        total_marks,

        duration="3 Hours"

    ):


        return {


            "title":
            "University Examination",


            "subject":
            subject,


            "duration":
            duration,


            "total_marks":
            total_marks,


            "sections":
            sections


        }