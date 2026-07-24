
"""
export_service.py
"""

from backend.ai_engine.paper_generation.paper_exporter import PaperExporter


class ExportService:

    def __init__(self):

        self.exporter = PaperExporter()

    def export_json(self, paper):

        return self.exporter.export_json(paper)

    def export_docx(self, paper, template_path=None):

        return self.exporter.export_docx(paper, template_path)

    def export_pdf(self, paper):

        return self.exporter.export_pdf(paper)


export_service = ExportService()
