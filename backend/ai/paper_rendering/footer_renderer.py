class FooterRenderer:


    def render(self, template):


        footer = template.get(
            "footer",
            {}
        )


        if not footer.get(
            "available",
            False
        ):

            return []


        return [

            "",

            "Signature",

            "Page Number"

        ]