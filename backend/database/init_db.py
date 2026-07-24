from backend.database.database import Base,engine

from backend.database.models.template import Template



def create_tables():

    Base.metadata.create_all(
        bind=engine
    )


if __name__=="__main__":

    create_tables()

    print(
        "Database tables created"
    )