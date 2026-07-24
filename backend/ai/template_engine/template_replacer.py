"""
Template Replacer

Injects new paper data
into existing template coordinates.
"""


class TemplateReplacer:



    def replace(
        self,
        template,
        paper_data
    ):


        questions = paper_data.get(
            "questions",
            []
        )


        q_index = 0



        for page in template["pages"]:


            for obj in page["objects"]:


                if not obj.get(
                    "dynamic",
                    False
                ):

                    continue



                placeholder = obj["placeholder"]



                if placeholder == "{{COURSE_CODE}}":

                    obj["text"] = (
                        "Course Code: "
                        +
                        paper_data["course_code"]
                    )



                elif placeholder == "{{COURSE_NAME}}":

                    obj["text"] = (
                        "Course Name: "
                        +
                        paper_data["course_name"]
                    )



                elif placeholder == "{{SEMESTER}}":

                    obj["text"] = (
                        paper_data["semester"]
                    )



                elif placeholder == "{{DATE}}":

                    obj["text"] = (
                        paper_data["date"]
                    )



                elif placeholder == "{{TIME}}":

                    obj["text"] = (
                        paper_data["time"]
                    )



                elif placeholder == "{{MAX_MARKS}}":

                    obj["text"] = (
                        "Max Marks: "
                        +
                        str(
                            paper_data["max_marks"]
                        )
                    )



                elif placeholder == "{{QUESTION}}":


                    if q_index < len(questions):

                        q = questions[q_index]


                        obj["text"] = q["text"]


                        q_index += 1



        return template