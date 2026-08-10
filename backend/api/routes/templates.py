
from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import uuid
import json

from backend.ai_engine.template_learning.template_learning_pipeline import (
    TemplateLearningPipeline
)

router = APIRouter(
    prefix="/api/templates",
    tags=["Templates"]
)

TEMPLATE_DIR = Path("templates")
TEMPLATE_DIR.mkdir(exist_ok=True)

saved_templates = []

# Built-in template directory
DEFAULT_TEMPLATE_DIR = (
    Path(__file__).resolve().parents[2] / "default_templates"
)

# RIT Template
RIT_TEMPLATE_PATH = DEFAULT_TEMPLATE_DIR / "rit_exam_template.json"

# DKTE Template
DKTE_TEMPLATE_PATH = DEFAULT_TEMPLATE_DIR / "dkte_exam_template.json"


def built_in_templates():
    """Return fixed built-in templates that are always available."""

    templates = []

    # Load RIT Template
    if RIT_TEMPLATE_PATH.exists():
        with open(RIT_TEMPLATE_PATH, encoding="utf-8") as template_file:
            templates.append(json.load(template_file))

    # Load DKTE Template
    if DKTE_TEMPLATE_PATH.exists():
        with open(DKTE_TEMPLATE_PATH, encoding="utf-8") as template_file:
            templates.append(json.load(template_file))

    return templates


@router.get("")
def get_templates():
    return [*built_in_templates(), *saved_templates]


@router.post("/upload")
async def upload_template(
    file: UploadFile = File(...)
):
    file_id = str(uuid.uuid4())

    file_path = TEMPLATE_DIR / f"{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    learned_template = None

    try:
        learned_template = TemplateLearningPipeline().learn(
            str(file_path)
        )
    except Exception as exc:
        learned_template = {
            "source_path": str(file_path),
            "learning_error": str(exc)
        }

    template = {
        "id": file_id,
        "template_name": file.filename,
        "file_path": str(file_path),
        "learned_template": learned_template,

        # The Generate Paper API accepts template_json.
        # Expose the learned layout/pattern through that field.
        "template_json": learned_template
    }

    saved_templates.append(template)

    return template
