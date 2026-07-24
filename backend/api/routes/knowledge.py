from fastapi import APIRouter
from fastapi import Depends

from backend.api.services.knowledge_service import knowledge_service

from backend.api.dependencies.roles import require_teacher


router = APIRouter(

    prefix="/knowledge",

    tags=["Knowledge Base"]

)


# -------------------------------------------------
# Knowledge Status
# -------------------------------------------------

@router.get("/status")
def status(

    current_user=Depends(require_teacher)

):

    knowledge = knowledge_service.get()


    if knowledge is None:

        return {

            "ready": False,

            "documents": 0,

            "checked_by": current_user["email"]

        }


    return {

        "ready": True,

        "documents": len(

            knowledge["knowledge_records"]

        ),

        "checked_by": current_user["email"]

    }



# -------------------------------------------------
# Health Check (Public)
# -------------------------------------------------

@router.get("/health")
def health():

    return {

        "module": "Knowledge Base",

        "status": "Ready"

    }