"""JSON command-line bridge used by the Node backend."""

from __future__ import annotations

import base64
import json
import logging
import sys
import time
from typing import Any

from .coverage_optimizer import build_question_paper_sets
from .document_export import export_docx, export_pdf
from .evaluation import evaluate_generation
from .question_generator import DEFAULT_MODEL, generate_question_bank
from .syllabus_parser import parse_syllabus_payload

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def _read_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    return json.loads(raw or "{}")


def main() -> int:
    envelope = _read_payload()
    action = envelope.get("action")
    payload = envelope.get("payload") or {}
    started_at = time.perf_counter()

    if action == "parse_syllabus":
        result = parse_syllabus_payload(payload)
        result["model"] = DEFAULT_MODEL
    elif action == "generate_questions":
        result = generate_question_bank(payload)
        result["evaluation"] = evaluate_generation(result.get("questions", []), payload.get("syllabus") or payload, started_at)
    elif action == "generate_paper":
        result = build_question_paper_sets(payload)
        result["model"] = DEFAULT_MODEL
        result["fallback"] = False
    elif action == "export_docx":
        result = {"base64": base64.b64encode(export_docx(payload)).decode("ascii"), "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
    elif action == "export_pdf":
        result = {"base64": base64.b64encode(export_pdf(payload)).decode("ascii"), "mimeType": "application/pdf"}
    else:
        raise ValueError(f"Unknown AI action: {action}")

    sys.stdout.write(json.dumps(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        sys.stderr.write(str(exc))
        raise SystemExit(1)
