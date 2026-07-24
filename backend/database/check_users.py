"""
Check QuestAI Users
"""

from backend.database.database import SessionLocal
from backend.models.user import User

# IMPORTANT:
# Import all models so SQLAlchemy relationships load correctly
from backend.models.uploaded_file import UploadedFile
from backend.models.question import Question
from backend.models.paper import QuestionPaper
from backend.models.history import History
from backend.models.subject import Subject
from backend.models.knowledge import Knowledge
from backend.models.upload import Upload
from backend.models.template import Template
from backend.models.material import Material


def check_users():

    print("\n======================")
    print("QUESTAI USERS")
    print("======================")

    db = SessionLocal()

    try:

        users = db.query(User).all()

        if not users:

            print("No users found in database")

            return


        for user in users:

            print("----------------------")

            print(
                "ID:",
                user.id
            )

            print(
                "Name:",
                user.full_name
            )

            print(
                "Email:",
                user.email
            )

            print(
                "Role:",
                user.role
            )

            print(
                "Active:",
                user.is_active
            )


        print("----------------------")

        print(
            "Total Users:",
            len(users)
        )


    except Exception as e:

        print("\nERROR:")
        print(e)


    finally:

        db.close()



if __name__ == "__main__":

    check_users()