"""
QuestAI Upload API

Teacher Workflow

1. Upload Syllabus
2. Upload Study Material
3. Upload Previous Paper

Question Bank will later be generated from
Syllabus + Study Material.
"""

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from backend.database.dependency import get_db

from backend.api.dependencies.auth import get_current_user

from backend.api.services.upload_service import UploadService
from backend.api.services.knowledge_service import knowledge_service
from backend.ai_engine.preprocessing.document_processor import DocumentExtractionError


from backend.models.uploaded_file import UploadedFile
from backend.models.subject import Subject


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

service = UploadService()


# ---------------------------------------
# Allowed File Extensions
# ---------------------------------------

ALLOWED_EXTENSIONS={

".pdf",

".doc",

".docx",

".ppt",

".pptx",

".txt",

".md",

".rtf",

".csv",

".xls",

".xlsx",

".jpg",

".jpeg",

".png",

".bmp",

".tif",

".tiff"

,
".html", ".htm", ".xml", ".json", ".odt", ".odp", ".ods", ".epub"

}


# ---------------------------------------
# Upload Categories
# ---------------------------------------

VALID_CATEGORIES = {
    "syllabus",
    "material",
    "previous_paper"
}


MAX_SIZE = 20 * 1024 * 1024
# =======================================================
# Get Teacher Uploaded Files
# =======================================================

@router.get("/files")
def get_uploaded_files(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    files = db.query(
        UploadedFile
    ).filter(

        UploadedFile.user_id == current_user["user_id"]

    ).all()


    result = []


    for file in files:

        result.append({

            "id": file.id,

            "filename": file.filename,

            "file_type": file.file_type,

            "category": file.upload_category,

            "subject_id": file.subject_id,

            "subject_name":
                file.subject.name
                if file.subject
                else None,

            "uploaded_at":
                file.uploaded_at

        })


    return result

# =======================================================
# Upload File
# =======================================================

@router.post("/")
async def upload_file(

    file: UploadFile = File(...),

    upload_category: str = Form(...),

    subject_id: int | None = Form(None),

    subject_name: str | None = Form(None),

    course_code: str | None = Form(None),

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    uploaded_file = None
    info = None
    try:

        print("\n==============================")
        print("UPLOAD REQUEST")
        print("==============================")

        print("File:", file.filename)

        print("Category:", upload_category)

        print("Subject ID:", subject_id)

        print("Subject Name:", subject_name)

        print("Course Code:", course_code)


        upload_category = upload_category.lower()



        # -----------------------------------
        # Validate Category
        # -----------------------------------

        if upload_category not in VALID_CATEGORIES:

            raise HTTPException(

                status_code=400,

                detail="Invalid upload category"

            )



        # -----------------------------------
        # Subject Handling
        # -----------------------------------

        subject = None



        # CASE 1:
        # Syllabus upload
        # Creates subject automatically

        if upload_category == "syllabus":


            if not subject_name or not course_code:

                raise HTTPException(

                    status_code=400,

                    detail="Subject name and course code required"

                )


            subject = db.query(Subject).filter(

                Subject.code == course_code

            ).first()



            if subject is None:


                subject = Subject(

                    name=subject_name,

                    code=course_code

                )


                db.add(subject)

                db.commit()

                db.refresh(subject)



            subject_id = subject.id



        # CASE 2:
        # Material / Previous Paper

        else:


            if subject_id is None:

                raise HTTPException(

                    status_code=400,

                    detail="Subject selection required"

                )



            subject = db.query(Subject).filter(

                Subject.id == subject_id

            ).first()



            if subject is None:

                raise HTTPException(

                    status_code=404,

                    detail="Subject not found"

                )



        # -----------------------------------
        # File Extension Validation
        # -----------------------------------

        suffix = "." + file.filename.split(".")[-1].lower()



        if suffix not in ALLOWED_EXTENSIONS:

            raise HTTPException(

                status_code=400,

                detail="Unsupported file type"

            )



        # -----------------------------------
        # File Size Validation
        # -----------------------------------

        content = await file.read()



        if len(content) > MAX_SIZE:

            raise HTTPException(

                status_code=400,

                detail="File exceeds 20 MB limit"

            )


        await file.seek(0)



        # -----------------------------------
        # Save Physical File
        # -----------------------------------

        info = service.save(file)



        # -----------------------------------
        # Save Database Record
        # -----------------------------------

        uploaded_file = UploadedFile(

            filename=info["filename"],

            filepath=info["path"],

            file_type=suffix,

            upload_category=upload_category,

            subject_id=subject.id,

            user_id=current_user["user_id"]

        )


        db.add(uploaded_file)

        db.commit()

        db.refresh(uploaded_file)



        # -----------------------------------
        # Knowledge Base Creation
        # -----------------------------------

        # ---------------------------------------
        # Knowledge Base Creation
        # ---------------------------------------

        knowledge = None


        # Syllabus upload
        # Only create initial knowledge base
        # NO Gemini call

        if upload_category == "syllabus":

            knowledge = knowledge_service.build_knowledge_only(

                info["path"],

                uploaded_file.id,

                db,

                subject.id

            )


        # Study Material upload
        # Combine with existing syllabus knowledge
        # NO Gemini call

        elif upload_category == "material":


            knowledge = knowledge_service.build_knowledge_only(

                info["path"],

                uploaded_file.id,

                db,

                subject.id

            )


        return {


            "success": True,


            "message":
                "Upload completed successfully",


            "subject": {

                "id": subject.id,

                "name": subject.name,

                "code": subject.code

            },


            "file": {

                "id": uploaded_file.id,

                "filename": uploaded_file.filename,

                "category": uploaded_file.upload_category,

                "type": uploaded_file.file_type

            },


            "knowledge": knowledge

        }



    except HTTPException:

        raise



    except DocumentExtractionError as e:
        # The record is created before processing because Knowledge rows need
        # its id. Do not leave an unusable upload behind when extraction fails.
        if uploaded_file is not None:
            db.delete(uploaded_file)
            db.commit()
        if info and info.get("path"):
            from pathlib import Path
            Path(info["path"]).unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=str(e)) from e

    except Exception as e:

        print("UPLOAD ERROR:", e)

        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail="Upload processing failed. Please try again or use a supported readable file.") from e
    
# =======================================================
# Get Uploaded Syllabi
# =======================================================

@router.get("/syllabi")
def get_uploaded_syllabi(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    files = db.query(

        UploadedFile

    ).filter(

        UploadedFile.user_id == current_user["user_id"],

        UploadedFile.upload_category == "syllabus"

    ).all()


    result = []


    for file in files:

        result.append({

            "id": file.subject_id,

            "subject_name": file.subject.name
                if file.subject else "",

            "course_code": file.subject.code
                if file.subject else "",

            "filename": file.filename

        })


    return result
# =======================================================
# Delete Uploaded File
# =======================================================

@router.delete("/files/{file_id}")
def delete_uploaded_file(

    file_id:int,

    db:Session=Depends(get_db),

    current_user=Depends(get_current_user)

):

    file=db.query(

        UploadedFile

    ).filter(

        UploadedFile.id==file_id,

        UploadedFile.user_id==current_user["user_id"]

    ).first()


    if file is None:

        raise HTTPException(

            status_code=404,

            detail="File not found"

        )


    import os


    if os.path.exists(file.filepath):

        os.remove(file.filepath)



    # remove knowledge base entries
    for knowledge in file.knowledge_records:

        db.delete(knowledge)



    db.delete(file)


    db.commit()


    return {

        "success":True,

        "message":"File deleted successfully"

    }

       
