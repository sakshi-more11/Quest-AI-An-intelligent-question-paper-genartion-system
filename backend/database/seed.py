from backend.database.database import SessionLocal, engine
from backend.database.base import Base


# ==================================================
# IMPORT ALL MODELS
# ==================================================

from backend.models.user import User
from backend.models.uploaded_file import UploadedFile
from backend.models.question import Question
from backend.models.paper import QuestionPaper
from backend.models.history import History
from backend.models.subject import Subject
from backend.models.knowledge import Knowledge
from backend.models.upload import Upload

from backend.models.template import Template
from backend.models.material import Material

# ==================================================
# PASSWORD HASH
# ==================================================

from backend.auth.password import hash_password



# ==================================================
# CREATE DATABASE TABLES
# ==================================================

Base.metadata.create_all(
    bind=engine
)



# ==================================================
# USER SEED DATA
# ==================================================

def seed_users():


    db = SessionLocal()



    users = [


        {
            "full_name": "System Admin",

            "email": "admin@questai.com",

            "password": "Admin@123",

            "role": "admin",

            "designation": "Administrator",

            "department": "Administration",

            "subject": "",

            "is_active": True
        },



        {
            "full_name": "Prof. Priya Sharma",

            "email": "teacher1@questai.com",

            "password": "teacher@123",

            "role": "teacher",

            "designation": "Assistant Professor",

            "department": "AI & ML",

            "subject": "Machine Learning",

            "is_active": True
        },



        {
            "full_name": "Prof. Arjun Verma",

            "email": "teacher2@questai.com",

            "password": "teacher@123",

            "role": "teacher",

            "designation": "Associate Professor",

            "department": "Computer Science",

            "subject": "Data Structures & Algorithms",

            "is_active": True
        }


    ]



    try:


        for user_data in users:



            existing = db.query(User).filter(
                User.email == user_data["email"]
            ).first()



            if existing:


                # Update existing user

                existing.full_name = user_data["full_name"]

                existing.password = hash_password(user_data["password"])
                

                existing.role = user_data["role"]

                existing.designation = user_data["designation"]

                existing.department = user_data["department"]

                existing.subject = user_data["subject"]

                existing.is_active = True



            else:


                # Create new user

                hashed_password = hash_password(
    user_data["password"]
)


                new_user = User(

                    full_name=user_data["full_name"],

                    email=user_data["email"],

                    password=hashed_password,

                    role=user_data["role"],

                    designation=user_data["designation"],

                    department=user_data["department"],

                    subject=user_data["subject"],

                    is_active=True
                )


                db.add(new_user)



        db.commit()


        print("✅ Users seeded successfully")



    except Exception as e:


        db.rollback()

        print("❌ Seed failed:", e)



    finally:


        db.close()




# ==================================================
# RUN SCRIPT
# ==================================================

if __name__ == "__main__":

    seed_users()