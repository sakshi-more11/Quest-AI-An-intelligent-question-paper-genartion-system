"""
QuestAI Question Generation Prompt Engine

Creates advanced engineering-level
question generation prompts.

Used by:
QuestionGenerationService
"""


class QuestionPromptBuilder:


    def __init__(self):

        pass



    # -------------------------------------------------
    # Main Prompt
    # -------------------------------------------------

    def build(

        self,

        subject_name,

        knowledge_context,

        number_of_questions=20

    ):


        prompt = f"""

You are an expert Engineering University Professor.

Generate university examination questions.

Subject:

{subject_name}


Reference Material:

{knowledge_context}



Generate {number_of_questions} questions.



STRICT RULES:

=================================================

1. ENGINEERING LEVEL

=================================================

Questions must be suitable for B.Tech engineering students.

Do NOT generate:

- simple definitions
- one line answers
- school level questions
- direct textbook statements


Prefer:

- analysis
- design
- implementation
- comparison
- optimization
- real-world scenarios
- numerical problems


=================================================

2. BLOOM TAXONOMY DISTRIBUTION

=================================================

Follow this distribution:

Remember:
5%

Understand:
20%

Apply:
25%

Analyze:
25%

Evaluate:
15%

Create:
10%



=================================================

3. DIFFICULTY DISTRIBUTION

=================================================

Easy:
20%

Medium:
50%

Hard:
30%



=================================================

4. QUESTION STYLE

=================================================


Include:

- Explain with architecture
- Analyze performance trade-offs
- Design solutions
- Compare algorithms
- Case-study based questions
- Numerical/problem solving questions


Avoid:

"What is..."

"Define..."

"List..."



=================================================

5. OUTPUT FORMAT

=================================================

Return ONLY valid JSON.

Format:


[
{{
"question":"",
"unit":"",
"marks":5,
"blooms_level":"",
"difficulty":"",
"question_type":"",
"expected_answer_points":""
}}
]


=================================================

Important:

Every question must be derived from the provided syllabus
and study material.


"""


        return prompt