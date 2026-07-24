from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import uuid
from backend.ai_engine.template_learning.template_learning_pipeline import TemplateLearningPipeline


router = APIRouter(
    prefix="/api/templates",
    tags=["Templates"]
)


TEMPLATE_DIR = Path("templates")

TEMPLATE_DIR.mkdir(exist_ok=True)


saved_templates = []



@router.get("")
def get_templates():

    return saved_templates



@router.post("/upload")
async def upload_template(
    file: UploadFile = File(...)
):

    file_id = str(uuid.uuid4())


    file_path = TEMPLATE_DIR / f"{file_id}_{file.filename}"


    with open(file_path,"wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    learned_template = None
    try:
        learned_template = TemplateLearningPipeline().learn(str(file_path))
    except Exception as exc:
        learned_template = {"source_path": str(file_path), "learning_error": str(exc)}

    template = {

        "id": file_id,

        "template_name": file.filename,

        "file_path": str(file_path),
        "learned_template": learned_template,
        # The Generate Paper API accepts template_json.  Expose the learned
        # layout/pattern through that established field without UI changes.
        "template_json": learned_template

    }


    saved_templates.append(template)


    return template
