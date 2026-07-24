"""
Authentication Schemas
"""

from pydantic import BaseModel
from pydantic import EmailStr


class RegisterRequest(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    role: str = "teacher"


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"

    role: str

    email: str

    name: str