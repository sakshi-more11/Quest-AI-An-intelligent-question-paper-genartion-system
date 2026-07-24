"""Bloom's Taxonomy classifier with Logistic Regression fallback support."""

from __future__ import annotations

import re
from typing import Any

BLOOM_LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

KEYWORDS = {
    "Remember": ["define", "list", "state", "name", "identify", "recall", "write"],
    "Understand": ["explain", "summarize", "describe", "classify", "compare", "interpret"],
    "Apply": ["solve", "use", "apply", "calculate", "demonstrate", "implement"],
    "Analyze": ["analyze", "differentiate", "derive", "inspect", "relate", "contrast"],
    "Evaluate": ["evaluate", "justify", "critique", "assess", "defend", "recommend"],
    "Create": ["design", "develop", "construct", "formulate", "propose", "create"],
}


class BloomClassifier:
    """Small classifier wrapper that uses sklearn when trained data is supplied."""

    def __init__(self) -> None:
        self.pipeline: Any | None = None

    def train(self, texts: list[str], labels: list[str]) -> None:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
            from sklearn.linear_model import LogisticRegression  # type: ignore
            from sklearn.pipeline import Pipeline  # type: ignore

            self.pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), stop_words="english")),
                ("clf", LogisticRegression(max_iter=1000)),
            ])
            self.pipeline.fit(texts, labels)
        except Exception:
            self.pipeline = None

    def predict(self, text: str) -> str:
        if self.pipeline:
            return str(self.pipeline.predict([text])[0])
        return classify_bloom(text)


def classify_bloom(text: str) -> str:
    normalized = text.lower()
    scores = {level: 0 for level in BLOOM_LEVELS}
    for level, words in KEYWORDS.items():
        for word in words:
            if re.search(rf"\b{re.escape(word)}\b", normalized):
                scores[level] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] else "Understand"
