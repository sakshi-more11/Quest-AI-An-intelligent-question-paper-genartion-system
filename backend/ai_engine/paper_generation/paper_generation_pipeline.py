"""
paper_generation_pipeline.py
"""


from backend.ai_engine.paper_generation.question_selector import QuestionSelector
from backend.ai_engine.paper_generation.marks_allocator import MarksAllocator
from backend.ai_engine.paper_generation.template_applier import TemplateApplier
from backend.ai_engine.paper_generation.paper_builder import PaperBuilder
from backend.ai_engine.paper_generation.paper_validator import PaperValidator
from backend.ai_engine.paper_generation.paper_exporter import PaperExporter

from backend.ai_engine.paper_generation.paper_response import PaperResponse
from backend.ai_engine.paper_generation.analytics import build_analytics



class PaperGenerationPipeline:


    def __init__(self):

        self.selector = QuestionSelector()

        self.marks_allocator = MarksAllocator()

        self.template = TemplateApplier()

        self.builder = PaperBuilder()

        self.validator = PaperValidator()

        self.exporter = PaperExporter()



    def generate(

        self,

        request

    ):


        # Select Questions

        selected = self.selector.select(request.generated_question_pool, request.marks_distribution,
                                        getattr(request, "syllabus_topics", None))


        # Allocate Marks

        allocated = self.marks_allocator.allocate(

            selected,

            request.total_marks

        )


        # Apply Template

        structured = self.template.apply(

            allocated["questions"],

            request.template

        )


        # Build Paper

        paper = self.builder.build(

            request.subject,

            structured["sections"],

            request.total_marks,

            request.duration

        )
        learned_template = request.template if isinstance(request.template, dict) else {}
        nested_template = learned_template.get("learned_template") or learned_template.get("template_json") or {}
        source_path = (learned_template.get("source_path") or learned_template.get("file_path") or
                       (nested_template.get("source_path") if isinstance(nested_template, dict) else None))
        if source_path:
            paper["template_path"] = source_path
        paper["template_blueprint"] = structured.get("blueprint", {})


        # Validate

        validation = self.validator.validate(paper)
        analytics = build_analytics(allocated["questions"], getattr(request, "syllabus_topics", None))
        validation["analytics"] = analytics


        # Export

        path = self.exporter.export_json(paper)
        docx_path = self.exporter.export_docx(paper, source_path)
        pdf_path = self.exporter.export_pdf(paper)


        return PaperResponse(

            paper=paper,

            total_marks=request.total_marks,

            validation_report=validation,

            export_paths={

                "json": path,
                "docx": docx_path,
                "pdf": pdf_path

            },

            success=validation["valid"],
            message="Paper Generated Successfully",

            analytics=analytics

        )
