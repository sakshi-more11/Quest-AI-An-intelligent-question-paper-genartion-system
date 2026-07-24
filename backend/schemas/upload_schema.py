from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):

    id: int

    teacher_id: int

    upload_type: str

    file_name: str

    file_path: str

    status: str

    created_at: datetime

    class Config:

        from_attributes = True