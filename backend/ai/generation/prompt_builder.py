def build_prompt(

    context,

    subject,

    unit,

    bloom,

    difficulty,

    marks,

    number_of_questions

):

    return f"""
You are an experienced university professor.

Generate exactly {number_of_questions} examination questions.

Subject:
{subject}

Unit:
{unit}

Bloom Level:
{bloom}

Difficulty:
{difficulty}

Marks:
{marks}

Use ONLY the following study material.

-------------------------

{context}

-------------------------

Rules:

1. Questions must be original.

2. No duplicate questions.

3. Do not copy text.

4. Use university examination style.

5. Return JSON only.

Format:

[
 {{

 "question":"",

 "marks":{marks},

 "difficulty":"{difficulty}",

 "bloom":"{bloom}"

 }}

]
"""