"""
export.py
"""

from pydantic import BaseModel
from typing import Optional


class ExportRequest(BaseModel):

    paper: dict
    template_path: Optional[str] = None
