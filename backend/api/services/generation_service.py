"""Application service for the verified OpenRouter question pipeline."""

from backend.ai_engine.question_generation.generation_pipeline import GenerationPipeline


class GenerationService:
    def __init__(self):
        self.pipeline = GenerationPipeline()

    def generate(self, request, context_records=None):
        return self.pipeline.generate(request, context_records)


generation_service = GenerationService()
