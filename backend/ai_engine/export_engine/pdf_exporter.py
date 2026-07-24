from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

import os



class PDFExporter:


    def export(self,paper,output_path):


        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )


        doc = SimpleDocTemplate(
            output_path
        )


        styles = getSampleStyleSheet()

        content=[]


        content.append(
            Paragraph(
                paper["title"],
                styles["Title"]
            )
        )


        content.append(
            Spacer(1,20)
        )


        for section in paper["sections"]:


            content.append(
                Paragraph(
                    section["name"],
                    styles["Heading2"]
                )
            )


            for q in section["questions"]:

                content.append(
                    Paragraph(
                        q["question"],
                        styles["Normal"]
                    )
                )

                content.append(
                    Spacer(1,10)
                )


        doc.build(content)


        return output_path