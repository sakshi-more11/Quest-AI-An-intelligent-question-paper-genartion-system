from pydantic import BaseModel, EmailStr


class TeacherCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    designation: str
    department: str
    subject: str


class TeacherUpdate(BaseModel):
    full_name: str
    designation: str
    department: str
    subject: str


class TeacherResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    designation: str
    department: str
    subject: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True