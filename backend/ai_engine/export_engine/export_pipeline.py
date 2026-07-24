from backend.ai_engine.export_engine.pdf_exporter import PDFExporter
from backend.ai_engine.export_engine.docx_exporter import DOCXExporter
from backend.ai_engine.export_engine.json_exporter import JSONExporter



class ExportPipeline:


    def __init__(self):

        self.pdf = PDFExporter()

        self.docx = DOCXExporter()

        self.json = JSONExporter()



    def export(self,paper):


        result={}


        result["pdf"] = self.pdf.export(
            paper,
            "exports/question_paper.pdf"
        )


        result["docx"] = self.docx.export(
            paper,
            "exports/question_paper.docx"
        )


        result["json"] = self.json.export(
            paper,
            "exports/question_paper.json"
        )


        return result