from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.database import SessionLocal
from backend.database.models.template import Template


router = APIRouter(
    prefix="/templates",
    tags=["Templates"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post("/upload")
def upload_template(
    data:dict,
    db:Session=Depends(get_db)
):


    template = Template(

        user_id=data.get(
            "user_id",
            1
        ),

        template_name=data[
            "template_name"
        ],

        template_json=data[
            "template_json"
        ]

    )


    db.add(template)

    db.commit()

    db.refresh(template)



    return {

        "message":
        "Template saved successfully",

        "template_id":
        template.id

    }





@router.get("/")
def get_templates(
    db:Session=Depends(get_db)
):


    templates=db.query(
        Template
    ).all()



    return templates





@router.delete("/{template_id}")
def delete_template(
    template_id:int,

    db:Session=Depends(get_db)

):


    template=db.query(
        Template
    ).filter(
        Template.id==template_id
    ).first()



    if template:

        db.delete(template)

        db.commit()



    return {

        "message":
        "Template deleted"

    }