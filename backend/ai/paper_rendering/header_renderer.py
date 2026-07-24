class HeaderRenderer:


    def render(self, template, metadata):

        header = []

        config = template.get(
            "header",
            {}
        )


        if not config.get(
            "available",
            False
        ):
            return header


        header.append(
            metadata.get(
                "college_name",
                ""
            )
        )


        header.append(
            metadata.get(
                "exam_name",
                ""
            )
        )


        header.append(
            ""
        )


        header.append(
            f"Course Code: {metadata.get('course_code','')}"
        )


        header.append(
            f"Course Name: {metadata.get('course_name','')}"
        )


        return header