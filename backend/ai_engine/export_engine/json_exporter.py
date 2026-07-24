import json
import os


class JSONExporter:


    def export(self, paper, output_path):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )


        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                paper,
                file,
                indent=4,
                ensure_ascii=False
            )


        return output_path