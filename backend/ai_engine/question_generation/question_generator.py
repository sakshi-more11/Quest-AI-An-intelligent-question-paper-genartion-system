"""LLM drafting followed by QuestAI's local ML/NLP verification modules."""

from backend.ai_engine.classifier.bloom_bert_classifier import BloomBERTClassifier
from backend.ai_engine.classifier.difficulty_classifier import DifficultyClassifier
from backend.ai_engine.question_generation.llm_client import LLMClient
from backend.ai_engine.question_generation.prompt_builder import PromptBuilder
from backend.ai_engine.question_generation.question_postprocessor import QuestionPostProcessor
from backend.ai_engine.question_generation.question_response import QuestionResponse


class QuestionGenerator:
    def __init__(self, llm_client=None, bloom_classifier=None, difficulty_classifier=None, co_mapper=None):
        self.llm = llm_client or LLMClient()
        self.prompt_builder = PromptBuilder()
        self.postprocessor = QuestionPostProcessor()
        self.bloom_classifier = bloom_classifier or BloomBERTClassifier()
        self.difficulty_classifier = difficulty_classifier or DifficultyClassifier()
        if co_mapper is not None:
            self.co_mapper = co_mapper
        else:
            try:
                from backend.ai_engine.co_mapping.co_mapper import COMapper
                self.co_mapper = COMapper()
            except Exception:
                # Generation must remain available when an optional local SBERT
                # artifact is unavailable; the response records no CO confidence.
                self.co_mapper = None

    def generate(self, request, context_records=None):
        context_records = context_records or []
        context = self._context_text(context_records)
        prompt = self.prompt_builder.build(request.subject, request.unit, request.bloom_level,
            request.difficulty, request.marks, request.question_type, context, request.number_of_questions)
        payload = self.llm.generate_json(prompt)
        raw_questions = payload.get("questions", []) if isinstance(payload, dict) else payload
        if not isinstance(raw_questions, list):
            raise ValueError("OpenRouter response must contain a questions array")
        verified = [self._verify(item, request) for item in self.postprocessor.clean(raw_questions)]
        verified = [item for item in verified if item]
        return QuestionResponse(verified[:request.number_of_questions], context_records, prompt,
            self.llm.model, bool(verified), "Questions generated and verified with local ML/NLP modules.")

    @staticmethod
    def _context_text(records):
        parts = [str(item.get("text") or item.get("content") or "") if isinstance(item, dict) else str(item)
                 for item in records]
        return "\n\n".join(part for part in parts if part)[:16000] or "No source context was retrieved."

    def _verify(self, item, request):
        item = item if isinstance(item, dict) else {"question": str(item)}
        text = str(item.get("question", "")).strip()
        if not text:
            return None
        marks = int(item.get("marks", request.marks) or request.marks)
        mapped = self.co_mapper.map_question(text) if self.co_mapper else {"co": item.get("co"), "confidence": None}
        return {"question": text, "marks": marks, "topic": item.get("topic") or request.unit,
                "unit": item.get("unit") or request.unit, "question_type": item.get("question_type") or request.question_type,
                "requested_bloom_level": request.bloom_level, "requested_difficulty": request.difficulty,
                "bloom_level": self.bloom_classifier.predict(text),
                "difficulty": self.difficulty_classifier.predict(text, marks),
                "co": mapped.get("co"), "co_confidence": mapped.get("confidence")}
