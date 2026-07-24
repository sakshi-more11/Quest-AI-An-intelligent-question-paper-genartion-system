"""
paper_response.py
"""

from dataclasses import dataclass, field


@dataclass
class PaperResponse:

    paper: list = field(default_factory=list)

    total_marks: int = 0

    validation_report: dict = field(default_factory=dict)

    export_paths: dict = field(default_factory=dict)

    success: bool = False

    message: str = ""

    analytics: dict = field(default_factory=dict)
