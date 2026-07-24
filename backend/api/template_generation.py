from fastapi import APIRouter, HTTPException

from backend.services.paper_generation_service import PaperGenerationService


router = APIRouter()



@router.post(
    "/generate-from-template"
)
def generate_paper(data: dict):

    try:

        service = PaperGenerationService()


        result = service.generate(

            template_id=data["template_id"],

            metadata=data["metadata"],

            questions=data["questions"]

        )


        return {

            "success": True,

            "message": "Paper generated successfully",

            "data": result

        }


    except KeyError as e:


        raise HTTPException(

            status_code=400,

            detail=f"Missing field: {str(e)}"

        )


    except Exception as e:


        return {

            "success": False,

            "error": str(e)

        }