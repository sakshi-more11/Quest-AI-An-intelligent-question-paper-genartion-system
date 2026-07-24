"""
paper.py

Question Paper Generation API
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from backend.api.dependencies.roles import require_teacher

from backend.api.schemas.paper import PaperRequest

from backend.api.services.paper_service import paper_service

from backend.database.database import SessionLocal

from backend.models.question import Question
from backend.ai_engine.paper_generation.ui_contract import build_sets
from backend.ai_engine.paper_generation.template_blueprint import blueprint_from_template


router = APIRouter(

    prefix="/paper",

    tags=["Question Paper"]

)


@router.post("/")
def generate_paper(

    request: PaperRequest,

    current_user=Depends(require_teacher)

):

    db = SessionLocal()

    try:

        # The submitted question-bank entries are the primary source.  The
        # database model stores subject as a relationship, so querying it by
        # a plain subject string here would crash the generation request.
        questions = db.query(Question).all()

        if not questions and not request.questions:

            raise HTTPException(

                status_code=404,

                detail="No generated questions found."

            )

        generated_question_pool = list(request.questions)

        for q in questions:

            generated_question_pool.append(

                {

                    "question": q.question_text,

                    "marks": q.marks,

                    "bloom_level": q.blooms_level,
                    "difficulty": q.difficulty,
                    "topic": q.unit,
                    "co": q.co_mapping,

                    "unit": q.unit

                }

            )

        # Inject generated questions into request
        request.generated_question_pool = generated_question_pool

        # A faculty upload is the paper contract.  There is intentionally no
        # default 50-mark / 2-5-10 fallback here.
        try:
            blueprint = blueprint_from_template(request.template, request.marks_distribution)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        sets, quality = build_sets(generated_question_pool, request.syllabus, request.template)
        # Set A is canonical.  Its marks and number/sub-question slots come
        # from the uploaded faculty template, never from a fixed UI blueprint.
        request.generated_question_pool = [question for section in sets["A"].values() for question in section]
        request.marks_distribution = blueprint["marks_distribution"]
        request.total_marks = blueprint["total_marks"]
        request.syllabus_topics = [topic for unit in (request.syllabus or {}).get("units", [])
                                   for topic in (unit.get("topics", []) or [unit.get("name")]) if topic]
        result = paper_service.generate(request)

        return {

            "success": True,

            "generated_by": current_user["email"],

            "role": current_user["role"],

            "paper": result.__dict__,
            "sets": sets,
            "quality": quality,
            "model": "OpenRouter"

        }

    finally:

        db.close()


@router.get("/health")
def health():

    return {

        "module": "Paper Generation",

        "status": "Ready"

    }
