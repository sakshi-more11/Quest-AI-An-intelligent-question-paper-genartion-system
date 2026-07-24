from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet



class PDFRenderer:



    def render(
        self,
        paper_data,
        output_path
    ):


        document = SimpleDocTemplate(
            output_path,
            pagesize=A4
        )


        styles = getSampleStyleSheet()


        elements=[]



        for line in paper_data:


            text = Paragraph(

                str(line),

                styles["Normal"]

            )


            elements.append(text)


            elements.append(
                Spacer(1,12)
            )



        document.build(
            elements
        )


        return output_path