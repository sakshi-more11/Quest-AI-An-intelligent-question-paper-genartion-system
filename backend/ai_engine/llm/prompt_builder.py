"""
QuestAI Prompt Builder

Creates controlled prompts
for question generation
"""


class PromptBuilder:



    def build(

        self,

        topic,

        bloom,

        difficulty,

        marks,

        context

    ):


        prompt = f"""

Generate an engineering examination question.

Topic:
{topic}


Bloom Level:
{bloom}


Difficulty:
{difficulty}


Marks:
{marks}


Related Questions:
{context}


Rules:
- Avoid duplicate questions
- Follow university pattern
- Maintain academic language

"""


        return prompt