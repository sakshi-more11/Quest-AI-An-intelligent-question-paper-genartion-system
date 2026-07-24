"""Local Bloom/difficulty metadata adapter.

Question drafting is the only OpenRouter task.  Classification intentionally
uses the project's existing fine-tuned BERT artefacts and never calls an LLM.
"""

import re


class BloomClassifier:
    def __init__(self):
        self._bloom = None
        self._difficulty = None

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
            return {
                "bloom_level": re.match(r"BT[1-6]", bloom["bloom_level"]).group(0),
                "difficulty": difficulty["difficulty"],
                "bloom_confidence": bloom.get("confidence"),
                "difficulty_confidence": difficulty.get("confidence"),
                "co_mapping": "",
            }
        except Exception:
            # The existing project has a lightweight deterministic classifier
            # for deployments where the BERT artefact cannot be loaded.
            from backend.ai_engine.classifier.bloom_bert_classifier import BloomBERTClassifier
            from backend.ai_engine.classifier.difficulty_classifier import DifficultyClassifier
            return {"bloom_level": BloomBERTClassifier().predict(text).replace("BL", "BT"),
                    "difficulty": DifficultyClassifier().predict(text, 7), "co_mapping": ""}
