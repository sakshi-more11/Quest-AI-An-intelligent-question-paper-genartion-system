from backend.ai.embeddings.embedder import create_embeddings

from backend.ai.embeddings.faiss_index import *

from backend.ai.generation.prompt_builder import build_prompt

from backend.ai.generation.question_generator import generate_questions


class QuestionGenerationService:


    def generate(

        self,

        subject,

        unit,

        bloom,

        difficulty,

        marks,

        count

    ):

        index = load_index()

        chunks = load_chunks()

        query = f"{subject} {unit}"

        query_embedding = create_embeddings(

            [query]

        )[0]

        retrieved = search(

            query_embedding,

            index,

            chunks,

            top_k=5

        )

        context = "\n\n".join(retrieved)

        prompt = build_prompt(

            context=context,

            subject=subject,

            unit=unit,

            bl=bloom,

            difficulty=difficulty,

            marks=marks,

            number_of_questions=count

        )

        return generate_questions(prompt)