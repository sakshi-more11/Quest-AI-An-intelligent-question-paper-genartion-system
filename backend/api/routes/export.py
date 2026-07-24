"""
export.py
"""

import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.api.schemas.export_models import ExportRequest

from backend.api.services.export_service import export_service


router = APIRouter(

    prefix="/export",

    tags=["Export"]

)


@router.post("/json")
def export_json(request: ExportRequest):

    path = export_service.export_json(request.paper)

    return {

        "success": True,

        "path": path

    }


@router.post("/docx")
def export_docx(request: ExportRequest):

    path = export_service.export_docx(

        request.paper,
        request.template_path

    )

    return {

        "success": True,

        "path": path

    }


@router.post("/pdf")
def export_pdf(request: ExportRequest):

    path = export_service.export_pdf(

        request.paper

    )

    return {

        "success": True,

        "path": path

    }


@router.get("/download/{filename}")
def download(filename: str):

    path = os.path.join(

        "exports",

        filename

    )

    return FileResponse(

        path,

        filename=filename

    )
