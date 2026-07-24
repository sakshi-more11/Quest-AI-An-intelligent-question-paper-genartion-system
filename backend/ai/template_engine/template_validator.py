"""
QuestAI Template Validator

Validates and normalizes templates.
"""


from backend.ai.template_engine.template_normalizer import (
    TemplateNormalizer
)



class TemplateValidator:



    def __init__(self):


        self.normalizer = TemplateNormalizer()




    def validate(self,template):


        report={


            "valid":True,


            "errors":[],


            "warnings":[]


        }


        if not isinstance(
            template,
            dict
        ):


            report["valid"]=False


            report["errors"].append(
                "Template must be dictionary"
            )


            return report



        return report





    def prepare(self,template):


        """
        Main function used by renderer
        """


        report=self.validate(
            template
        )



        if not report["valid"]:


            raise Exception(
                report
            )



        normalized = self.normalizer.normalize(
            template
        )


        return normalized