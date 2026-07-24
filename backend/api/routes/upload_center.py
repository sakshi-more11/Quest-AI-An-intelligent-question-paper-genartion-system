from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import Depends

from sqlalchemy.orm import Session

from pathlib import Path
import shutil

from backend.database.database import get_db
from backend.models.material import Material

router = APIRouter(
    prefix="/materials",
    tags=["Upload Center"]
)

UPLOAD_DIR = Path("storage/uploads/materials")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/upload")
async def upload_material(

    subject: str = Form(...),

    uploaded_by: int = Form(...),

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    teacher_folder = UPLOAD_DIR / f"teacher_{uploaded_by}"

    teacher_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    save_path = teacher_folder / file.filename

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    material = Material(

        filename=file.filename,

        original_name=file.filename,

        file_type=file.filename.split(".")[-1],

        subject=subject,

        uploaded_by=uploaded_by,

        path=str(save_path)

    )

    db.add(material)

    db.commit()

    db.refresh(material)

    return {

        "success": True,

        "material_id": material.id

    }