"""
question_bank_builder.py

Phase 11
AI Question Bank Generator

Input:
    Retrieved chunks from Knowledge Base

Output:
    35-40 Engineering Questions
"""


import json
from backend.ai_engine.bloom_classifier.bloom_classifier import BloomClassifier
from backend.ai_engine.question_generation.llm_client import LLMClient
from backend.ai_engine.question_generation.question_postprocessor import QuestionPostProcessor



class QuestionBankBuilder:


    def __init__(self):

        self.classifier = BloomClassifier()

        self.client = LLMClient()
        self.model = self.client.model
        self.postprocessor = QuestionPostProcessor()



    # ----------------------------------------------------
    # Prompt Creation
    # ----------------------------------------------------

    def build_prompt(self, chunks):


        texts = []


        for chunk in chunks:

            if isinstance(chunk, dict):

                texts.append(
                    chunk.get("text","")
                )

            else:

                texts.append(
                    str(chunk)
                )


        context = "\n\n".join(texts)


        prompt = f"""

You are an expert Engineering University Question Paper Setter.

Using ONLY the provided study material,
create a high-quality engineering question bank.


==========================
QUESTION GENERATION RULES
==========================


Generate EXACTLY 40 questions. Keep each JSON object compact: do not include
answers, explanations, rationales, citations, or extra fields.


Questions must be suitable for B.Tech engineering students.


Follow university examination standards.


Rules:

- Questions must be technically accurate.
- Avoid meaningless generic questions.
- Avoid repeated questions.
- Avoid very short questions.
- Avoid extremely lengthy questions.
- Never begin a question with "Explain in detail". Use a precise academic
  task verb matched to the Bloom level (for example: Compare, Analyse,
  Design, Derive, Evaluate, or Discuss).
- Never turn headers, course outcomes, bibliography, URLs, names, or pasted
  notes into questions.
- Use proper engineering terminology.
- Use a balanced mix of: derivation/analysis, algorithm tracing, numerical
  problem formulation, architecture/design trade-offs, debugging or failure
  analysis, and comparison under stated constraints.
- Anchor every question to a named concept, method, component, or measurable
  condition found in the material. State assumptions or inputs when needed.
- Include numerical/design-oriented questions wherever the material permits;
  do not manufacture numbers or facts absent from it.
- Vary opening verbs and sentence patterns. "Explain", "Describe", and
  "Discuss" together may start no more than 8 questions.
- Marks should be from 5 to 10.Not all questions should have same marks.
- CO i.e Course Outcomes re present in the syllabus file take CO from there.
Example-CO1: Fundamentals
CO2: Algorithms/Techniques
CO3: Applications
CO4: Analysis and Design
Question length: 12-32 words. Each question must end with a question mark or
be an unambiguous examination instruction.



==========================
BLOOM DISTRIBUTION
==========================


BT1 Remember:
4 questions


BT2 Understand:
10 questions


BT3 Apply:
10 questions


BT4 Analyze:
8 questions


BT5 Evaluate:
5 questions


BT6 Create:
3 questions



BT1 and BT6 should be limited.

Most questions should belong to BT2-BT5.



==========================
DIFFICULTY DISTRIBUTION
==========================


Easy:
10


Medium:
20


Hard:
10



==========================
OUTPUT FORMAT
==========================


Return ONLY a valid JSON object with a "questions" array.

No markdown.

Format:


{{ "questions": [
 {{
 "question":
 "Explain process scheduling algorithms and compare their performance.",
 
 "unit":
 "Unit 2",
 
 "bloom_level":
 "BT4",
 
 "difficulty":
 "Medium",
 
 "marks":
 7
 }}
] }}


Every object must contain:

question

unit

bloom_level

difficulty

marks



==========================
STUDY MATERIAL
==========================


{context}


"""


        return prompt



    # ----------------------------------------------------
        # OpenRouter generation (the sole LLM used by QuestAI).
    # ----------------------------------------------------

    # ----------------------------------------------------
# OpenRouter Generation
# ----------------------------------------------------

    def generate(self, chunks):

        prompt = self.build_prompt(chunks)


        try:

            payload = self.client.generate_json(prompt, required_key="questions", minimum_items=40)
            questions = payload.get("questions", []) if isinstance(payload, dict) else payload
            if not isinstance(questions, list):
                raise ValueError("OpenRouter did not return a questions array")


            questions = self.postprocessor.clean(questions)
            if not questions:
                raise ValueError("OpenRouter returned no valid engineering questions")
            print(f"Generated using OpenRouter model {self.model}")


        except Exception as e:


            # Never use the legacy local fallback: it converts source text to
            # "Explain in detail" questions and corrupts the bank.
            raise RuntimeError(f"OpenRouter question generation failed: {e}") from e



        for q in questions:


            metadata=self.classifier.classify(q["question"])


            q["bloom_level"]=metadata.get(
                "bloom_level",
                q.get(
                    "bloom_level",
                    "BT2"
                )
            )


            q["difficulty"]=metadata.get(
                "difficulty",
                q.get(
                    "difficulty",
                    "Medium"
                )
            )


            q["co_mapping"]=metadata.get(
                "co_mapping",
                ""
            )
            q["bloom_confidence"] = metadata.get("bloom_confidence")
            q["difficulty_confidence"] = metadata.get("difficulty_confidence")


        return questions
