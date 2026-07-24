from fastapi import APIRouter

router = APIRouter(
    prefix="/analyze",
    tags=["Paper Analysis"]
)


@router.get("/health")
def health():

    return {
        "module": "Paper Analysis",
        "status": "Ready"
    }