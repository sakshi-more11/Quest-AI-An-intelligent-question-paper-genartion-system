"""Compatibility adapter for the established Generate Paper screen contract."""

from collections import Counter
from difflib import SequenceMatcher
from backend.ai_engine.paper_generation.analytics import build_analytics
from backend.ai_engine.paper_generation.template_blueprint import blueprint_from_template
from backend.ai_engine.quality.bloom_mapper import BloomMapper


_BLOOM_MAPPER = BloomMapper()


def _normalise(question):
    text = question.get("question") or question.get("text") or question.get("question_text") or ""
    bloom_level = _BLOOM_MAPPER.classify(text)
    return {
        "question": text,
        "unit": question.get("unit") or "Auto",
        "topic": question.get("topic") or question.get("unit") or "Auto",
        "bloom_level": bloom_level,
        "difficulty": "Easy" if bloom_level == "BT1" else question.get("difficulty") or "Medium",
        "co": question.get("co") or question.get("co_mapping"),
    }


def build_sets(question_pool, syllabus=None, template=None):
    candidates = [_normalise(question) for question in question_pool]
    candidates = [question for question in candidates if question["question"].strip()]
    blueprint = blueprint_from_template(template)
    sets, cursor, used_globally = {}, 0, []
    for label in ("A", "B", "C"):
        paper_set, used = {}, []
        bt1_count = 0
        required_slots = blueprint["required_slots"]
        bloom_cap = max(1, len(required_slots) // 5)
        difficulty_targets = _difficulty_targets(len(required_slots))
        for section, slots in blueprint["sections"].items():
            values = []
            for slot in slots:
                available = [candidate for candidate in candidates if candidate["bloom_level"] != "BT1" or bt1_count < 1]
                available = [candidate for candidate in available if all(
                    SequenceMatcher(None, candidate["question"].lower(), other["question"].lower()).ratio() < 0.88
                    for other in used + used_globally)]
                # A bank smaller than all three sets may reuse across sets, but
                # never within a single paper.
                if not available:
                    available = [candidate for candidate in candidates if (candidate["bloom_level"] != "BT1" or bt1_count < 1) and all(
                        SequenceMatcher(None, candidate["question"].lower(), other["question"].lower()).ratio() < 0.88 for other in used)]
                # Never leave an uploaded-template slot empty merely because
                # the semantic matcher considers two different questions too
                # similar.  Prefer a different literal question in the same
                # set; cross-set reuse is already allowed above.
                if not available:
                    available = [candidate for candidate in candidates if (candidate["bloom_level"] != "BT1" or bt1_count < 1) and candidate["question"] not in {
                        other["question"] for other in used
                    }]
                if not available:
                    break
                question = dict(_choose_balanced_candidate(
                    available, used, slot, bloom_cap, difficulty_targets
                ))
                cursor += 1
                question["marks"] = slot["marks"]
                question["question_no"] = slot["question_no"]
                question["sub_question"] = slot["sub_question"]
                question["choice_group"] = slot.get("choice_group")
                question["selection_group"] = slot.get("selection_group")
                question["required_count"] = slot.get("required_count", 1)
                # Template CO remains authoritative, while Bloom must reflect
                # the actual question task rather than a fixed slot label.
                question["co"] = slot.get("co") or question.get("co")
                question["bloom"] = question["bloom_level"]
                question["or_before"] = bool(slot.get("choice_group") and values and
                                             values[-1].get("choice_group") == slot.get("choice_group"))
                values.append(question)
                used.append(question)
                used_globally.append(question)
                bt1_count += question["bloom_level"] == "BT1"
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


def _difficulty_targets(total):
    """Use the requested engineering-paper balance: 30% Easy, 40% Medium, 30% Hard."""
    easy = round(total * 0.30)
    hard = round(total * 0.30)
    return {"Easy": easy, "Medium": total - easy - hard, "Hard": hard}


def _choose_balanced_candidate(available, used, slot, bloom_cap, difficulty_targets):
    """Select for a balanced paper; template Bloom labels are preferences, not mandates."""
    bloom_counts = Counter(question.get("bloom_level") for question in used)
    difficulty_counts = Counter(question.get("difficulty") for question in used)
    preferred_bloom = str(slot.get("bloom") or "").upper().replace("BL", "BT")
    underrepresented = min(
        (level for level in ("BT2", "BT3", "BT4", "BT5", "BT6")),
        key=lambda level: bloom_counts[level],
    )
    desired_bloom = preferred_bloom if preferred_bloom in {"BT2", "BT3", "BT4", "BT5", "BT6"} and bloom_counts[preferred_bloom] < bloom_cap else underrepresented
    desired_difficulty = min(
        (level for level in ("Easy", "Medium", "Hard")),
        key=lambda level: difficulty_counts[level] / max(1, difficulty_targets[level]),
    )
    wants_scenario = len(used) % 3 == 1

    def score(candidate):
        text = candidate["question"].lower()
        is_scenario = any(word in text for word in ("scenario", "case", "given", "dataset", "real-world", "fault", "constraint"))
        return (
            candidate["bloom_level"] != desired_bloom,
            bloom_counts[candidate["bloom_level"]],
            candidate["difficulty"] != desired_difficulty,
            difficulty_counts[candidate["difficulty"]] >= difficulty_targets.get(candidate["difficulty"], 0),
            wants_scenario and not is_scenario,
            candidate["question"].lower(),
        )

    return min(available, key=score)


def _section_key(section):
    # Keep the legacy UI contract for ordinary A/B/C templates while preserving
    # arbitrary faculty section labels for exports and API clients.
    label = str(section).strip().upper()
    return {"A": "sectionA", "B": "sectionB", "C": "sectionC"}.get(label, "section" + label.replace(" ", "") if label != "GENERAL" else "sectionA")
