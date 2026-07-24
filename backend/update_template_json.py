from backend.database.database import SessionLocal
from backend.models.template import Template


db = SessionLocal()


template = db.query(Template).filter(
    Template.id == 1
).first()


template.template_json = {


    "college": {

        "name": "Rajarambapu Institute of Technology"

    },


    "header": {

        "available": True,

        "alignment": "center",

        "font": "Times New Roman",

        "size": 14

    },


    "question_format": {


        "numbering": "Q1",

        "parts": [

            "A",

            "B"

        ],

        "marks_position": "right"


    },


    "layout": {


        "margin": "1 inch",

        "spacing": 1.5,

        "page_size": "A4"


    },


    "footer": {


        "available": True,


        "signature": True,


        "page_number": True


    },


    "typography": {


        "font": "Times New Roman",

        "question_size": 12


    }



}


db.commit()


print("Template Updated Successfully")


db.close()