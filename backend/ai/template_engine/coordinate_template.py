import json



class CoordinateTemplate:


    def create(self, extracted_objects):


        template = {

            "pages":[]

        }



        for page in extracted_objects:


            page_template={


                "page_number":page["page"],


                "objects":[]


            }



            for obj in page["objects"]:


                page_template["objects"].append({


                    "text":obj["text"],

                    "x":int(obj["x"]),

                    "y":int(obj["y"]),


                    "width":int(obj["width"]),


                    "height":int(obj["height"]),


                    "font":obj.get(
                        "font",
                        "Unknown"
                    ),


                    "font_size":float(
                        obj["font_size"]
                    ),


                    "bold":self.detect_bold(
                        obj["text"],
                        obj["font_size"]
                    ),


                    "alignment":
                    self.detect_alignment(
                        obj
                    )


                })



            template["pages"].append(
                page_template
            )



        return template





    def save(
        self,
        template,
        path
    ):


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(

                template,

                f,

                indent=4

            )





    def detect_bold(
        self,
        text,
        size
    ):


        keywords=[

            "Course Code",

            "Course Name",

            "Instruction",

            "Q."

        ]


        if size > 65:

            return True


        for k in keywords:

            if k.lower() in text.lower():

                return True


        return False






    def detect_alignment(
        self,
        obj
    ):


        page_width=2500


        center = (
            obj["x"] + obj["width"]/2
        )


        if abs(
            center-page_width/2
        ) < 200:


            return "center"


        elif center > page_width/2:


            return "right"


        return "left"