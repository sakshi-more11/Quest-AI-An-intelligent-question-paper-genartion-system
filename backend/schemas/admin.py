from pydantic import BaseModel, EmailStr


class TeacherCreate(BaseModel):

    full_name: str
    email: EmailStr
    password: str


class TeacherResponse(BaseModel):

    id: int
    full_name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True