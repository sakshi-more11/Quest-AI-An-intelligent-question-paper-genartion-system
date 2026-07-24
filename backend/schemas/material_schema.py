from pydantic import BaseModel


class MaterialResponse(BaseModel):

    id: int

    filename: str

    original_name: str

    subject: str

    file_type: str

    uploaded_at: str

    class Config:

        from_attributes = True