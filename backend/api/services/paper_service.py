"""
paper_service.py
"""

from backend.ai_engine.paper_generation.paper_generation_pipeline import (
    PaperGenerationPipeline
)


class PaperService:

    def __init__(self):

        self.pipeline = PaperGenerationPipeline()

    def generate(self, request):

        return self.pipeline.generate(request)


paper_service = PaperService()