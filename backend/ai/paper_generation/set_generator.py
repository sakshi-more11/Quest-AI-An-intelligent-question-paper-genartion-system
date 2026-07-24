class PaperSetGenerator:

    def __init__(

        self,

        service

    ):

        self.service = service

    def generate_sets(

        self,

        blueprint

    ):

        set_a = self.service.select_questions(

            blueprint

        )

        set_b = self.service.select_questions(

            blueprint

        )

        set_c = self.service.select_questions(

            blueprint

        )

        return {

            "A": set_a,

            "B": set_b,

            "C": set_c

        }