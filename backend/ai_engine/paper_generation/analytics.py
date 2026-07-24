"""Deterministic paper analytics used by generation and the evaluation API."""

from collections import Counter
from difflib import SequenceMatcher


def _percentages(values):
    total = sum(values.values())
    return {key: round(value * 100 / total, 2) for key, value in values.items()} if total else {}


def pairwise_similarity(questions):
    texts = [str(question.get("question", "")).lower() for question in questions]
    scores = [SequenceMatcher(None, left, right).ratio() for index, left in enumerate(texts) for right in texts[index + 1:]]
    return round(max(scores, default=0.0) * 100, 2), round(sum(score >= 0.88 for score in scores) * 100 / len(scores), 2) if scores else 0.0


def build_analytics(questions, syllabus_topics=None):
    topics = Counter(str(question.get("topic") or question.get("unit") or "Unmapped") for question in questions)
    bloom = Counter(str(question.get("bloom_level") or "Unmapped") for question in questions)
    difficulty = Counter(str(question.get("difficulty") or "Unmapped") for question in questions)
    co = Counter(str(question.get("co") or "Unmapped") for question in questions)
    max_similarity, duplicate_percent = pairwise_similarity(questions)
    target_topics = {str(topic) for topic in (syllabus_topics or []) if topic}
    coverage = round(len(set(topics) & target_topics) * 100 / len(target_topics), 2) if target_topics else 100.0
    confidences = [float(question["co_confidence"]) for question in questions if question.get("co_confidence") is not None]
    bloom_confidences = [float(question["bloom_confidence"]) for question in questions if question.get("bloom_confidence") is not None]
    difficulty_confidences = [float(question["difficulty_confidence"]) for question in questions if question.get("difficulty_confidence") is not None]
    return {
        "syllabus_coverage_percent": coverage,
        "covered_topics": sorted(topics),
        "uncovered_topics": sorted(target_topics - set(topics)),
        "bloom_distribution": _percentages(bloom),
        "difficulty_distribution": _percentages(difficulty),
        "co_coverage": {"covered": sorted(key for key in co if key != "Unmapped"), "distribution": _percentages(co)},
        "similarity_score": max_similarity,
        "duplicate_percent": duplicate_percent,
        "confidence_metrics": {"co_mapping_mean": round(sum(confidences) / len(confidences), 4) if confidences else None,
                               "questions_with_co_confidence": len(confidences),
                               "bloom_mean": round(sum(bloom_confidences) / len(bloom_confidences), 4) if bloom_confidences else None,
                               "difficulty_mean": round(sum(difficulty_confidences) / len(difficulty_confidences), 4) if difficulty_confidences else None,
                               "validated_questions": len(questions)},
    }
