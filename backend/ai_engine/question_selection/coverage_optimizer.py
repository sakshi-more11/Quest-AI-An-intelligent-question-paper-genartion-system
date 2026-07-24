"""Coverage, marks and multi-set optimization."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .bloom_classifier import BLOOM_LEVELS, classify_bloom
from .difficulty_predictor import predict_difficulty
from .similarity_checker import find_duplicates, similarity_score

DEFAULT_STRUCTURE = {
    "sectionA": {"marks": 2, "count": 5},
    "sectionB": {"marks": 5, "count": 4},
    "sectionC": {"marks": 10, "count": 2},
}


def flatten_syllabus_topics(syllabus: dict[str, Any]) -> list[str]:
    topics: list[str] = []
    for unit in syllabus.get("units") or []:
        if unit.get("name"):
            topics.append(unit["name"])
        topics.extend(unit.get("topics") or [])
    return [topic for topic in topics if topic]


def coverage_metrics(questions: list[dict], syllabus: dict[str, Any]) -> dict[str, Any]:
    topics = flatten_syllabus_topics(syllabus)
    if not topics:
        return {"topicsDetected": 0, "topicsCovered": 0, "syllabusCoverageScore": 0}
    question_text = " ".join((q.get("text") or q.get("question") or "") for q in questions)
    covered = [topic for topic in topics if similarity_score(topic, question_text) >= 0.12 or topic.lower() in question_text.lower()]
    return {
        "topicsDetected": len(topics),
        "topicsCovered": len(covered),
        "coveredTopics": covered,
        "syllabusCoverageScore": round((len(covered) / len(topics)) * 100, 2),
    }


def enrich_question(question: dict[str, Any], default_marks: int = 5) -> dict[str, Any]:
    text = question.get("text") or question.get("question") or ""
    marks = int(question.get("marks") or default_marks)
    bloom = question.get("bloom") or classify_bloom(text)
    return {
        **question,
        "text": text,
        "question": question.get("question") or text,
        "marks": marks,
        "bloom": bloom,
        "difficulty": question.get("difficulty") or predict_difficulty(text, marks, bloom),
        "co": question.get("co") or "CO1",
    }


def optimize_question_bank(questions: list[dict], syllabus: dict[str, Any]) -> dict[str, Any]:
    enriched = [enrich_question(q) for q in questions if (q.get("text") or q.get("question"))]
    unique, duplicate_pairs = find_duplicates(enriched)
    coverage = coverage_metrics(unique, syllabus)
    bloom_counts = Counter(q.get("bloom") for q in unique)
    difficulty_counts = Counter(q.get("difficulty") for q in unique)
    duplicate_score = round((len(unique) / max(1, len(enriched))) * 100, 2)
    overall = round(duplicate_score * 0.35 + coverage["syllabusCoverageScore"] * 0.45 + min(100, len(bloom_counts) / 6 * 100) * 0.2, 2)
    return {
        "questions": unique,
        "removedDuplicates": len(enriched) - len(unique),
        "duplicatePairs": duplicate_pairs,
        "quality": {
            **coverage,
            "duplicatePreventionScore": duplicate_score,
            "semanticAlignmentScore": coverage["syllabusCoverageScore"],
            "unitDistributionScore": _unit_distribution(unique),
            "overallAccuracy": overall,
            "bloomDistribution": dict(bloom_counts),
            "difficultyDistribution": dict(difficulty_counts),
        },
    }


def _unit_distribution(questions: list[dict]) -> float:
    units = {q.get("unit") for q in questions if q.get("unit")}
    return round(min(100, len(units) / max(1, len(questions) / 3) * 100), 2)


def build_question_paper_sets(payload: dict[str, Any]) -> dict[str, Any]:
    syllabus = payload.get("syllabus") or {}
    bank = [enrich_question(q) for q in (payload.get("questions") or [])]
    if len(bank) < 33:
        from .question_generator import fallback_questions

        bank.extend(fallback_questions(syllabus, count=36 - len(bank)))
    bank = optimize_question_bank(bank, syllabus)["questions"]
    by_marks: dict[int, list[dict]] = defaultdict(list)
    for q in bank:
        by_marks[int(q.get("marks") or 5)].append(q)

    used_texts: list[str] = []
    sets: dict[str, dict[str, list[dict]]] = {}
    for set_name in ("A", "B", "C"):
        sets[set_name] = {}
        for section, spec in DEFAULT_STRUCTURE.items():
            selected = _select_questions(by_marks[spec["marks"]], spec["count"], used_texts, syllabus, spec["marks"])
            used_texts.extend(q["question"] for q in selected)
            sets[set_name][section] = selected

    all_questions = [
        {"text": q["question"], **q}
        for paper_set in sets.values()
        for section_questions in paper_set.values()
        for q in section_questions
    ]
    quality = optimize_question_bank(all_questions, syllabus)
    return {"sets": sets, "quality": quality["quality"], "removedDuplicates": quality["removedDuplicates"], "duplicatePairs": quality["duplicatePairs"]}


def _select_questions(pool: list[dict], count: int, used_texts: list[str], syllabus: dict[str, Any], marks: int) -> list[dict]:
    selected: list[dict] = []
    topics = flatten_syllabus_topics(syllabus) or ["core concepts"]
    candidates = sorted(pool, key=lambda q: (q.get("unit") or "", q.get("bloom") or ""))
    for candidate in candidates:
        text = candidate.get("question") or candidate.get("text") or ""
        if all(similarity_score(text, used) < 0.78 for used in used_texts + [q["question"] for q in selected]):
            selected.append(_paper_question(candidate, marks))
        if len(selected) == count:
            return selected
    while len(selected) < count:
        topic = topics[(len(selected) + len(used_texts)) % len(topics)]
        bloom = BLOOM_LEVELS[(len(selected) + marks) % len(BLOOM_LEVELS)]
        text = f"{bloom} a practical scenario involving {topic} and justify the key steps."
        selected.append(_paper_question({"text": text, "unit": topic, "bloom": bloom}, marks))
    return selected


def _paper_question(question: dict[str, Any], marks: int) -> dict[str, Any]:
    text = question.get("question") or question.get("text") or ""
    bloom = question.get("bloom") or classify_bloom(text)
    return {
        "question": text,
        "marks": marks,
        "unit": question.get("unit") or "General",
        "bloom": bloom,
        "difficulty": question.get("difficulty") or predict_difficulty(text, marks, bloom),
        "co": question.get("co") or "CO1",
    }
