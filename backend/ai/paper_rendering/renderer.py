from .header_renderer import HeaderRenderer
from .question_renderer import QuestionRenderer
from .footer_renderer import FooterRenderer



class PaperRenderer:


    def __init__(self):

        self.header = HeaderRenderer()

        self.questions = QuestionRenderer()

        self.footer = FooterRenderer()



    def render(
        self,
        template,
        metadata,
        questions
    ):


        paper=[]


        # HEADER

        paper.extend(

            self.header.render(
                template,
                metadata
            )

        )


        paper.append(
            "\n"
        )


        # QUESTIONS

        paper.extend(

            self.questions.render(
                questions
            )

        )


        # FOOTER

        paper.extend(

            self.footer.render(
                template
            )

        )


        return paper