from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials


from backend.auth.jwt_handler import verify_access_token



security = HTTPBearer()



# ==================================================
# GET CURRENT USER
# ==================================================

async def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(security)

):


    token = credentials.credentials



    payload = verify_access_token(token)



    if payload is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid token"

        )



    return {

        "user_id": payload.get("user_id"),

        "email": payload.get("email"),

        "role": payload.get("role")

    }




# ==================================================
# ADMIN ONLY
# ==================================================

async def admin_required(

    current_user = Depends(get_current_user)

):


    if current_user["role"] != "admin":


        raise HTTPException(

            status_code=403,

            detail="Admin access required"

        )


    return current_user