"""
upload_service.py

Handles file uploads.
"""

from pathlib import Path
import shutil
from uuid import uuid4


class UploadService:

    def __init__(self):

        self.upload_dir = Path("backend/uploads")

        self.upload_dir.mkdir(

            parents=True,

            exist_ok=True

        )

    def save(

        self,

        file

    ):

        # Different teachers frequently upload files with the same name.
        # Keep a safe unique storage name while retaining the original name in
        # the database/UI.
        suffix = Path(file.filename or "upload").suffix.lower()
        destination = self.upload_dir / f"{uuid4().hex}{suffix}"

        with open(destination, "wb") as buffer:

            shutil.copyfileobj(

                file.file,

                buffer

            )

        return {

            "filename": Path(file.filename or "upload").name,

            "path": str(destination),

            "size": destination.stat().st_size

        }
