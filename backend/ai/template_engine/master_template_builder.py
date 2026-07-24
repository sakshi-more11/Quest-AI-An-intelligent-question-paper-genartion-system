"""
Master Template Builder

Creates the complete reusable template
using classified coordinate objects.
"""


class MasterTemplateBuilder:

    def build(self, classified_data):

        template = {

            "pages": []

        }

        for page in classified_data["pages"]:

            page_template = {

                "page": page["page"],
                "objects": []

            }

            for obj in page["objects"]:

                page_template["objects"].append({

                    "type": obj["type"],

                    "text": obj["text"],

                    "x": obj["x"],

                    "y": obj["y"],

                    "width": obj["width"],

                    "height": obj["height"],

                    "font": obj["font"],

                    "font_size": obj["font_size"],

                    "flags": obj["flags"]

                })

            template["pages"].append(page_template)

        return template