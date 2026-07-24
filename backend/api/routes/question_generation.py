from fastapi import APIRouter

from pydantic import BaseModel

from backend.services.question_generation_service import QuestionGenerationService

router = APIRouter(

    prefix="/ai",

    tags=["AI Question Generation"]

)

service = QuestionGenerationService()


class GenerateRequest(BaseModel):

    subject:str

    unit:str

    bloom:str

    difficulty:str

    marks:int

    count:int


@router.post("/generate")

def generate(

    request:GenerateRequest

):

    return service.generate(

        subject=request.subject,

        unit=request.unit,

        bl=request.bloom,

        difficulty=request.difficulty,

        marks=request.marks,

        count=request.count

    )