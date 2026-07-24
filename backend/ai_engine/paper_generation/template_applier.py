"""Apply the learned faculty-paper structure to already selected questions."""

from backend.ai_engine.paper_generation.template_blueprint import blueprint_from_template


class TemplateApplier:
    def apply(self, questions, template=None):
        blueprint = blueprint_from_template(template)
        sections, index = [], 0
        for name, slots in blueprint["sections"].items():
            rendered = []
            active_choice = None
            for slot in slots:
                if index >= len(questions):
                    break
                question = dict(questions[index])
                question.update({"marks": slot["marks"], "question_no": slot["question_no"],
                                 "sub_question": slot["sub_question"]})
                group = slot.get("choice_group")
                question["or_before"] = bool(group and group == active_choice)
                active_choice = group
                rendered.append(question)
                index += 1
            sections.append({"name": "Section " + str(name), "questions": rendered})
        return {"sections": sections, "blueprint": blueprint}
