from backend.ai_engine.question_generation.question_generator import QuestionGenerator


class GenerationPipeline:


    def __init__(self):

        self.generator = QuestionGenerator()


    def generate(self, request, context_records=None):
        return self.generator.generate(request, context_records)
