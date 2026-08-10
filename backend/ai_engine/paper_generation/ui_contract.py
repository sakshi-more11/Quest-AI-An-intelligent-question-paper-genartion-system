"""Compatibility adapter for the established Generate Paper screen contract."""

from difflib import SequenceMatcher
from backend.ai_engine.paper_generation.analytics import build_analytics
from backend.ai_engine.paper_generation.template_blueprint import blueprint_from_template


def _normalise(question):
    return {
        "question": question.get("question") or question.get("text") or question.get("question_text") or "",
        "unit": question.get("unit") or "Auto",
        "topic": question.get("topic") or question.get("unit") or "Auto",
        "bloom_level": question.get("bloom_level") or question.get("bloom") or question.get("blooms_level") or "BT2",
        "difficulty": question.get("difficulty") or "Medium",
        "co": question.get("co") or question.get("co_mapping"),
    }


def build_sets(question_pool, syllabus=None, template=None):
    candidates = [_normalise(question) for question in question_pool]
    candidates = [question for question in candidates if question["question"].strip()]
    blueprint = blueprint_from_template(template)
    sets, cursor, used_globally = {}, 0, []
    for label in ("A", "B", "C"):
        paper_set, used = {}, []
        for section, slots in blueprint["sections"].items():
            values = []
            for slot in slots:
                available = [candidate for candidate in candidates if all(
                    SequenceMatcher(None, candidate["question"].lower(), other["question"].lower()).ratio() < 0.88
                    for other in used + used_globally)]
                # A bank smaller than all three sets may reuse across sets, but
                # never within a single paper.
                if not available:
                    available = [candidate for candidate in candidates if all(
                        SequenceMatcher(None, candidate["question"].lower(), other["question"].lower()).ratio() < 0.88 for other in used)]
                # Never leave an uploaded-template slot empty merely because
                # the semantic matcher considers two different questions too
                # similar.  Prefer a different literal question in the same
                # set; cross-set reuse is already allowed above.
                if not available:
                    available = [candidate for candidate in candidates if candidate["question"] not in {
                        other["question"] for other in used
                    }]
                if not available:
                    break
                question = dict(available[cursor % len(available)])
                cursor += 1
                question["marks"] = slot["marks"]
                question["question_no"] = slot["question_no"]
                question["sub_question"] = slot["sub_question"]
                question["choice_group"] = slot.get("choice_group")
                question["selection_group"] = slot.get("selection_group")
                question["required_count"] = slot.get("required_count", 1)
                # The fixed university template owns the displayed CO and BT
                # columns.  An uploaded-question value remains the fallback.
                question["co"] = slot.get("co") or question.get("co")
                question["bloom"] = slot.get("bloom") or question["bloom_level"]
                question["or_before"] = bool(slot.get("choice_group") and values and
                                             values[-1].get("choice_group") == slot.get("choice_group"))
                values.append(question)
                used.append(question)
                used_globally.append(question)
            paper_set[_section_key(section)] = values
        sets[label] = paper_set
    topics = []
    for unit in (syllabus or {}).get("units", []):
        topics.extend(unit.get("topics", []) or [unit.get("name")])
    all_questions = [question for paper_set in sets.values() for values in paper_set.values() for question in values]
    metrics = build_analytics(all_questions, topics)
    quality = {
        "duplicatePreventionScore": round(100 - metrics["duplicate_percent"], 2),
        "syllabusCoverageScore": metrics["syllabus_coverage_percent"],
        "semanticAlignmentScore": round(100 - metrics["similarity_score"] / 4, 2),
        "overallAccuracy": round((100 - metrics["duplicate_percent"] + metrics["syllabus_coverage_percent"] + (100 - metrics["similarity_score"] / 4)) / 3, 2),
        "analytics": metrics,
    }
    quality["templateDriven"] = blueprint["template_driven"]
    quality["templateMarksDistribution"] = blueprint["marks_distribution"]
    quality["templateTotalMarks"] = blueprint["total_marks"]
    return sets, quality


def _section_key(section):
    # Keep the legacy UI contract for ordinary A/B/C templates while preserving
    # arbitrary faculty section labels for exports and API clients.
    label = str(section).strip().upper()
    return {"A": "sectionA", "B": "sectionB", "C": "sectionC"}.get(label, "section" + label.replace(" ", "") if label != "GENERAL" else "sectionA")
