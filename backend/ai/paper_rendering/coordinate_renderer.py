class CoordinateRenderer:

    def draw_text(
        self,
        canvas,
        text,
        x,
        y,
        font_name="Times-Roman",
        font_size=12,
        bold=False
    ):

        if bold:
            font_name = "Times-Bold"

        canvas.setFont(
            font_name,
            font_size
        )

        canvas.drawString(
            x,
            y,
            text
        )