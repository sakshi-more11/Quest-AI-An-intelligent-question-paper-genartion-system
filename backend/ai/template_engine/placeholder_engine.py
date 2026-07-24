class PlaceholderEngine:



    def replace_metadata(
        self,
        blocks,
        metadata
    ):


        replacements={


        "Course Code":
        "Course Code: "
        +
        metadata["course_code"],


        "Course Name":
        "Course Name: "
        +
        metadata["course_name"],


        "Max Marks":
        "Max Marks: "
        +
        str(metadata["max_marks"])


        }



        updated=[]


        for block in blocks:


            text=block["text"]


            for old,new in replacements.items():


                if old in text:


                    text=new



            block["text"]=text


            updated.append(block)



        return updated