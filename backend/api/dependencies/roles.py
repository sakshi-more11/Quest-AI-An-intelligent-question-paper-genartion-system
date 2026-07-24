"""
Role Based Authorization
"""

from fastapi import Depends
from fastapi import HTTPException

from backend.api.dependencies.auth import get_current_user


def require_teacher(

    current_user=Depends(get_current_user)

):

    if current_user["role"] not in [

        "teacher",

        "admin"

    ]:

        raise HTTPException(

            status_code=403,

            detail="Teacher access required"

        )

    return current_user



def require_admin(

    current_user=Depends(get_current_user)

):

    if current_user["role"] != "admin":

        raise HTTPException(

            status_code=403,

            detail="Admin access required"

        )

    return current_user