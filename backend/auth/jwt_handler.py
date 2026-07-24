"""
JWT Token Utilities
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt

from backend.api.core.config import settings



# -------------------------------------------------
# JWT Configuration
# -------------------------------------------------

SECRET_KEY = settings.JWT_SECRET_KEY

ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)



# -------------------------------------------------
# Create Access Token
# -------------------------------------------------

def create_access_token(
    data: dict
):

    to_encode = data.copy()


    expire = (
        datetime.now(timezone.utc)
        +
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


    to_encode.update(
        {
            "exp": expire
        }
    )


    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM

    )


    return encoded_jwt




# -------------------------------------------------
# Verify / Decode Token
# -------------------------------------------------

def verify_access_token(

    token: str

):

    try:


        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )


        return payload


    except JWTError:


        return None