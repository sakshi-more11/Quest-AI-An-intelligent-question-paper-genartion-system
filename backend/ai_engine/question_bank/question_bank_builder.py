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
- Include numerical/design-oriented questions wherever the material permits.
  Never copy worked-example operands or answers from the material (for example,
  do not repeat "2 + 3"). Create an equivalent assessment with different,
  sensible values (for example, "4 + 5") while preserving the same concept.
- Vary opening verbs and sentence patterns. "Explain", "Describe", and
  "Discuss" together may start no more than 8 questions.
- Marks should be from 5 to 10.Not all questions should have same marks.
- Use only these approved Bloom verbs and label the question from its first
  cognitive task: BT1 Define/List/Identify/Recall/Name/State/Label/Match/
  Recognize/Select/Reproduce/Quote/Memorize/Duplicate/Repeat/Record/Locate/
  Cite/Outline/Enumerate; BT2 Explain/Paraphrase/Report/Describe/Summarize/
  Interpret/Classify/Discuss/Restate/Translate/Compare/Illustrate/Infer/
  Predict/Estimate/Give examples/Rephrase/Review/Express/Clarify; BT3
  Practice/Calculate/Implement/Operate/Use/Illustrate/Solve/Demonstrate/
  Employ/Execute/Apply/Sketch/Interpret/Modify/Relate/Show/Utilize/Compute/
  Perform/Change; BT4 Compare/Contrast/Categorize/Organize/Distinguish/
  Differentiate/Examine/Investigate/Deconstruct/Correlate/Break down/Test/
  Question/Diagram/Inspect/Attribute/Discriminate/Outline/Subdivide/Detect;
  BT5 Assess/Judge/Defend/Prioritize/Critique/Recommend/Justify/Appraise/
  Argue/Validate/Conclude/Rate/Support/Interpret/Score/Evaluate/Decide/
  Debate/Rank/Verify; BT6 Invent/Develop/Design/Compose/Generate/Construct/
  Formulate/Devise/Plan/Produce/Synthesize/Assemble/Propose/Author/Build/
  Combine/Originate/Draft/Innovate/Compile. Shared verbs must use their task
  context: scenarios/data use BT3; comparing relationships uses BT4.
- Include at least 12 scenario-based questions across BT3--BT6. Each must
  state a realistic engineering case, condition, input, fault, or constraint
  and ask the student to act on it; do not use scenario wording for BT1.
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
1 question maximum (zero or one is acceptable)


BT2 Understand:
11 questions


BT3 Apply:
10 questions


BT4 Analyze:
8 questions


BT5 Evaluate:
5 questions


BT6 Create:
5 questions



BT1 and BT6 should be limited.

Most questions should belong to BT2-BT5.



==========================
DIFFICULTY DISTRIBUTION
==========================


Easy:
12


Medium:
16


Hard:
12



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
