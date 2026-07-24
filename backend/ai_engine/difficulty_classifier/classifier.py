"""Difficulty prediction using Random Forest when sklearn is available."""

from __future__ import annotations

from typing import Any

from .bloom_classifier import BLOOM_LEVELS

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]


class DifficultyPredictor:
    def __init__(self) -> None:
        self.model: Any | None = None

    def train_default(self) -> None:
        try:
            from sklearn.ensemble import RandomForestClassifier  # type: ignore

            rows = []
            labels = []
            for marks in (2, 5, 10):
                for bloom_index, bloom in enumerate(BLOOM_LEVELS):
                    length = 8 + marks * 2 + bloom_index
                    rows.append(_features(length, marks, bloom))
                    labels.append(_heuristic(length, marks, bloom))
            self.model = RandomForestClassifier(n_estimators=80, random_state=42)
            self.model.fit(rows, labels)
        except Exception:
            self.model = None

    def predict(self, text: str, marks: int = 5, bloom: str = "Understand") -> str:
        if self.model is None:
            self.train_default()
        if self.model:
            return str(self.model.predict([_features(len(text.split()), marks, bloom)])[0])
        return _heuristic(len(text.split()), marks, bloom)


def _features(length: int, marks: int, bloom: str) -> list[float]:
    bloom_index = BLOOM_LEVELS.index(bloom) if bloom in BLOOM_LEVELS else 1
    return [float(length), float(marks), float(bloom_index)]


def _heuristic(length: int, marks: int, bloom: str) -> str:
    score = 0
    score += 0 if marks <= 2 else 1 if marks <= 5 else 2
    score += 0 if length < 14 else 1 if length < 28 else 2
    score += 2 if bloom in {"Analyze", "Evaluate", "Create"} else 1 if bloom == "Apply" else 0
    if score <= 1:
        return "Easy"
    if score <= 3:
        return "Medium"
    return "Hard"


def predict_difficulty(text: str, marks: int = 5, bloom: str = "Understand") -> str:
    return DifficultyPredictor().predict(text, marks, bloom)
