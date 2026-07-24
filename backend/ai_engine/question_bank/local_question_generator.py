import random

class LocalQuestionGenerator:

    def generate(self, chunks):

        questions = []

        texts = []

        for chunk in chunks:

            if isinstance(chunk, dict):

                text = chunk.get("text", "")

            else:

                text = str(chunk)

            texts.extend(text.split("."))

        texts = [t.strip() for t in texts if len(t.strip()) > 30]

        if len(texts) == 0:

            texts = [
                "Explain the concepts covered in the uploaded syllabus."
            ]

        bloom_levels = [
            "BT1",
            "BT2",
            "BT3",
            "BT4",
            "BT5",
            "BT6"
        ]

        difficulties = [
            "Easy",
            "Medium",
            "Hard"
        ]

        marks_choices = [5, 6, 7, 8, 9, 10]

        for i in range(40):

            source = texts[i % len(texts)]

            questions.append({

                "question":
                    f"Explain in detail: {source}",

                "unit":
                    f"Unit {(i % 5) + 1}",

                "bloom_level":
                    random.choice(bloom_levels),

                "difficulty":
                    random.choice(difficulties),

                "marks":
                    random.choice(marks_choices)

            })

        print("Generated Questions: 40 (Local)")

        return questions