"""Turn a learned faculty-template pattern into a paper blueprint.

The blueprint is deliberately data-only so selection, analytics, DOCX export,
and PDF export all use the exact same question slots and marks.
"""

from collections import OrderedDict


def blueprint_from_template(template, fallback=None):

    if fallback is None:
        fallback = {}

    if not isinstance(template, dict):
        raise ValueError(
            "Template blueprint missing. Upload a valid template."
        )
    learned = template.get("learned_template") or template.get("template_json") or template
    pattern = learned.get("pattern", {}) if isinstance(learned, dict) else {}
    if not pattern:
        raise ValueError(
            "Uploaded template could not be parsed."
        )

    sections = OrderedDict()
    seen = set()
    raw_slots = learned.get("slots") if isinstance(learned, dict) else None
    entries = raw_slots if isinstance(raw_slots, list) else [
        dict(item, question_no=question_no)
        for question_no, alternatives in pattern.items() for item in (alternatives or [])
        if isinstance(item, dict)
    ]
    for item in entries:
            if not isinstance(item, dict):
                continue
            # A repeated question number/subpart is normally an OR option.
            slot_key = (str(item.get("section") or "General"), str(item.get("question_no") or ""),
                        str(item.get("sub_question") or ""), str(item.get("alternative") or ""))
            if slot_key in seen:
                continue
            seen.add(slot_key)
            section = str(item.get("section") or "General")
            sections.setdefault(section, []).append({
                "question_no": str(item.get("question_no") or ""),
                "sub_question": str(item.get("sub_question") or ""),
                "marks": int(item.get("marks") or 0),
                "choice_group": item.get("choice_group"),
                "selection_group": item.get("selection_group"),
                "required_count": int(item.get("required_count") or 1),
                "co": item.get("co"),
                "bloom": item.get("bloom"),
            })
    slots = [slot for section in sections.values() for slot in section if slot["marks"] > 0]
    if not slots:
        raise ValueError(
            "No question slots detected from uploaded template."
        )
    required_slots = _required_slots(slots)
    return {"sections": sections, "slots": slots, "required_slots": required_slots,
            "marks_distribution": _distribution(required_slots),
            "total_marks": sum(slot["marks"] for slot in required_slots), "template_driven": True}


def _from_distribution(distribution):
    slots = []
    for marks, count in distribution.items():
        slots.extend({"question_no": "", "sub_question": "", "marks": int(marks)} for _ in range(int(count)))
    return {"sections": OrderedDict([("General", slots)]), "slots": slots,
            "marks_distribution": _distribution(slots),
            "total_marks": sum(slot["marks"] for slot in slots), "template_driven": False}


def _distribution(slots):
    values = {}
    for slot in slots:
        values[slot["marks"]] = values.get(slot["marks"], 0) + 1
    return values


def _required_slots(slots):
    """OR alternatives are displayed, but only one contributes to paper marks."""
    required, seen_choices, selected_counts = [], set(), {}
    for slot in slots:
        selection_group = slot.get("selection_group")
        if selection_group:
            selected = selected_counts.get(selection_group, 0)
            if selected >= slot.get("required_count", 1):
                continue
            selected_counts[selection_group] = selected + 1
            required.append(slot)
            continue
        group = slot.get("choice_group")
        if group and group in seen_choices:
            continue
        if group:
            seen_choices.add(group)
        required.append(slot)
    return required
