from backend.database.database import SessionLocal

# Load ALL models (same as main.py)
import backend.models.user
import backend.models.subject
import backend.models.uploaded_file
import backend.models.knowledge
import backend.models.question
import backend.models.paper
import backend.models.history
import backend.models.material


from backend.models.question import Question


db = SessionLocal()


questions = db.query(Question).all()


print("Total Questions:", len(questions))


for q in questions[:5]:

    print("\n------------------")

    print("Question:")
    print(q.question_text)

    print("Bloom Level:", q.blooms_level)

    print("Difficulty:", q.difficulty)

    print("Marks:", q.marks)


db.close()