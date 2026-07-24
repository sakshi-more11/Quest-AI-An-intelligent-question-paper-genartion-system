from backend.database.database import SessionLocal
from backend.models.template import Template



class TemplateService:


    def get_template(self, template_id):


        db = SessionLocal()


        try:

            template = (
                db.query(Template)
                .filter(
                    Template.id == template_id
                )
                .first()
            )


            if not template:

                raise Exception(
                    "Template not found"
                )


            return template


        finally:

            db.close()

        get_template_config()    