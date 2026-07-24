"""
Authentication Routes
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db

from backend.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from backend.services.auth_service import AuthService

from backend.auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

auth_service = AuthService()


# --------------------------------------------------
# Register
# --------------------------------------------------

@router.post("/register")
def register(

    request: RegisterRequest,

    db: Session = Depends(get_db)

):

    try:

        user = auth_service.register(

            db=db,

            full_name=request.full_name,

            email=request.email,

            password=request.password,

            role=request.role

        )

        return {

            "message": "User registered successfully",

            "user_id": user.id,

            "email": user.email

        }

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# --------------------------------------------------
# Login
# --------------------------------------------------

@router.post(

    "/login",

    response_model=TokenResponse

)

def login(

    request: LoginRequest,

    db: Session = Depends(get_db)

):

    user = auth_service.login(

        db=db,

        email=request.email,

        password=request.password

    )

    if user is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )

    token = create_access_token(

        {

            "user_id": user.id,

            "email": user.email,

            "role": user.role

        }

    )

    return TokenResponse(

        access_token=token,

        role=user.role,

        email=user.email,

        name=user.full_name

)