"""
Dynamic Placeholder Manager

Finds editable fields inside template
and replaces only those fields.
"""


class PlaceholderManager:


    def __init__(self):

        self.dynamic_fields = {

            "course_code":
            "{{COURSE_CODE}}",

            "course_name":
            "{{COURSE_NAME}}",

            "semester":
            "{{SEMESTER}}",

            "date":
            "{{DATE}}",

            "time":
            "{{TIME}}",

            "max_marks":
            "{{MAX_MARKS}}",

            "question":
            "{{QUESTION}}",

            "marks":
            "{{MARKS}}",

            "co":
            "{{CO}}",

            "bl":
            "{{BL}}"

        }



    def convert_template(
        self,
        coordinate_template
    ):


        for page in coordinate_template["pages"]:


            for obj in page["objects"]:


                obj_type = self.get_type(obj)


                if obj_type in self.dynamic_fields:


                    obj["placeholder"] = (
                        self.dynamic_fields[obj_type]
                    )

                    obj["dynamic"] = True


                else:

                    obj["placeholder"] = None

                    obj["dynamic"] = False



        return coordinate_template





    def get_type(
        self,
        obj
    ):


        text = obj["text"].lower()



        if "course code" in text:

            return "course_code"



        if "course name" in text:

            return "course_name"



        if "semester" in text:

            return "semester"



        if "date" in text:

            return "date"



        if "time" in text:

            return "time"



        if "max marks" in text:

            return "max_marks"



        if text.startswith("q."):

            return "question"



        if text.startswith("co"):

            return "co"



        if text.startswith("bl"):

            return "bl"



        return None