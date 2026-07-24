"""
QuestAI AI Question Generator

Uses RAG + LLM
"""


from backend.ai_engine.llm.llm_client import (
    LLMClient
)


from backend.ai_engine.llm.prompt_builder import (
    PromptBuilder
)




class AIQuestionGenerator:



    def __init__(self):


        self.llm = LLMClient()


        self.prompt_builder = PromptBuilder()





    def generate_question(

        self,

        topic,

        bloom,

        difficulty,

        marks,

        context

    ):



        prompt = self.prompt_builder.build(

            topic,

            bloom,

            difficulty,

            marks,

            context

        )



        generated_question = self.llm.generate(prompt)

        return {

            "text": generated_question,

            "marks": marks,

            "bl": bloom,

            "difficulty": difficulty,

            "generated_by": "AI"

        }