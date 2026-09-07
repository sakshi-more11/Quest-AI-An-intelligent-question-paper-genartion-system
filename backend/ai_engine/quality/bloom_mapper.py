"""Deterministic Bloom taxonomy mapping using QuestAI's approved verbs only."""

import re


class BloomMapper:
    """Classify from the question's first cognitive task, not incidental words."""

    VERBS = {
        "BT1": ("define", "list", "identify", "recall", "name", "state", "label", "match", "recognize", "select", "reproduce", "quote", "memorize", "duplicate", "repeat", "record", "locate", "cite", "outline", "enumerate"),
        "BT2": ("explain", "paraphrase", "report", "describe", "summarize", "interpret", "classify", "discuss", "restate", "translate", "compare", "illustrate", "infer", "predict", "estimate", "give examples", "rephrase", "review", "express", "clarify"),
        "BT3": ("practice", "calculate", "implement", "operate", "use", "illustrate", "solve", "demonstrate", "employ", "execute", "apply", "sketch", "interpret", "modify", "relate", "show", "utilize", "compute", "perform", "change"),
        "BT4": ("analyze", "analyse", "compare", "contrast", "categorize", "organize", "distinguish", "differentiate", "examine", "investigate", "deconstruct", "correlate", "break down", "test", "question", "diagram", "inspect", "attribute", "discriminate", "outline", "subdivide", "detect"),
        "BT5": ("assess", "judge", "defend", "prioritize", "critique", "recommend", "justify", "appraise", "argue", "validate", "conclude", "rate", "support", "interpret", "score", "evaluate", "decide", "debate", "rank", "verify"),
        "BT6": ("create", "invent", "develop", "design", "compose", "generate", "construct", "formulate", "devise", "plan", "produce", "synthesize", "assemble", "propose", "author", "build", "combine", "originate", "draft", "innovate", "compile"),
    }
    _SCENARIO = re.compile(r"\b(case|scenario|given|using|dataset|data|problem|simulate|real[- ]world)\b", re.I)
    _ANALYTICAL = re.compile(r"\b(relationship|component|factor|cause|structure|pattern|difference)\b", re.I)
    _EVALUATIVE = re.compile(r"\b(criteria|justify|recommend|defend|best|trade[- ]?off|effectiveness)\b", re.I)

    def __init__(self):
        self._verb_levels = {}
        for level, verbs in self.VERBS.items():
            for verb in verbs:
                self._verb_levels.setdefault(verb, []).append(level)
        self._patterns = {
            verb: re.compile(r"(?<!\w)" + re.escape(verb) + r"(?:s|d|ed|ing)?(?!\w)", re.I)
            for verb in self._verb_levels
        }

    def classify(self, question):
        text = str(question or "").strip()
        if not text:
            return "BT2"
        matches = [(match.start(), verb) for verb, pattern in self._patterns.items() if (match := pattern.search(text))]
        if not matches:
            return "BT3" if self._SCENARIO.search(text) else "BT2"
        _, verb = min(matches, key=lambda item: item[0])
        levels = self._verb_levels[verb]
        return levels[0] if len(levels) == 1 else self._resolve_shared_verb(verb, text, levels)

    def _resolve_shared_verb(self, verb, text, levels):
        """Resolve only overlaps in the supplied list from task context."""
        scenario = bool(self._SCENARIO.search(text))
        if verb == "compare":
            return "BT4"
        if verb == "outline":
            return "BT4" if self._ANALYTICAL.search(text) else "BT1"
        if verb == "interpret":
            if self._EVALUATIVE.search(text):
                return "BT5"
            return "BT3" if scenario else "BT2"
        if verb == "illustrate":
            return "BT3" if scenario else "BT2"
        return levels[0]

    def map_questions(self, questions):
        for question in questions:
            level = self.classify(question.get("question", question.get("question_text", "")))
            question["blooms_level"] = level
            question["bloom_level"] = level
            if level == "BT1":
                question["difficulty"] = "Easy"
        return questions
