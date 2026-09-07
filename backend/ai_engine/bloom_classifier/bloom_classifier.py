"""Local Bloom/difficulty metadata adapter.

Question drafting is the only OpenRouter task.  Classification intentionally
uses the project's existing fine-tuned BERT artefacts and never calls an LLM.
"""

from backend.ai_engine.quality.bloom_mapper import BloomMapper


class BloomClassifier:
    def __init__(self):
        self._bloom = None
        self._difficulty = None
        self._mapper = BloomMapper()

    def classify(self, question):
        text = str(question or "").strip()
        if not text:
            return {"bloom_level": "BT2", "difficulty": "Medium", "co_mapping": ""}
        try:
            if self._bloom is None:
                from backend.ai.validation.bloom_classifier import predict_bloom
                from backend.ai.validation.difficulty_classifier import predict_difficulty
                self._bloom, self._difficulty = predict_bloom, predict_difficulty
            bloom = self._bloom(text)
            difficulty = self._difficulty(text)
            bloom_level = self._mapper.classify(text)
            return {
                "bloom_level": bloom_level,
                "difficulty": "Easy" if bloom_level == "BT1" else difficulty["difficulty"],
                "bloom_confidence": bloom.get("confidence"),
                "difficulty_confidence": difficulty.get("confidence"),
                "co_mapping": "",
            }
        except Exception:
            # The existing project has a lightweight deterministic classifier
            # for deployments where the BERT artefact cannot be loaded.
            from backend.ai_engine.classifier.difficulty_classifier import DifficultyClassifier
            bloom_level = self._mapper.classify(text)
            return {"bloom_level": bloom_level,
                    "difficulty": "Easy" if bloom_level == "BT1" else DifficultyClassifier().predict(text, 7), "co_mapping": ""}
