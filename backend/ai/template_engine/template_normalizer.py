"""
QuestAI Template Normalizer

Converts any template format
into standard QuestAI format.
"""


import copy


from backend.ai.template_engine.template_schema import (
    DEFAULT_TEMPLATE_SCHEMA
)



class TemplateNormalizer:



    def normalize(self, template):


        if not isinstance(template,dict):

            template={}



        final = copy.deepcopy(
            DEFAULT_TEMPLATE_SCHEMA
        )



        self.merge(
            final,
            template
        )



        self.fix_types(
            final
        )



        return final




    # ---------------------------------

    def merge(self,base,new):


        for key,value in new.items():


            if (

                isinstance(value,dict)

                and

                isinstance(base.get(key),dict)

            ):


                self.merge(

                    base[key],

                    value

                )


            else:


                base[key]=value





    # ---------------------------------

    def fix_types(self,template):


        """
        Prevent wrong datatype crashes
        """



        typography = template.get(
            "typography",
            {}
        )


        for section in [

            "header",

            "metadata",

            "question"

        ]:


            data = typography.get(
                section,
                {}
            )


            if not isinstance(
                data.get("font"),
                str
            ):


                data["font"] = (

                    "Times-Bold"

                    if section=="header"

                    else

                    "Times-Roman"

                )



        header = template.get(
            "header",
            {}
        )


        if not isinstance(
            header.get("font"),
            str
        ):


            header["font"]="Times-Bold"




        template["header"]=header