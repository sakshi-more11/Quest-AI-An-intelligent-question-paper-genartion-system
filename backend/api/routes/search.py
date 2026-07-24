from fastapi import APIRouter

from backend.ai_engine.vector_db.vector_store import VectorStore

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

store = VectorStore()


def get_vector_store():

    try:

        store.load(
            "storage/vector_db"
        )

    except FileNotFoundError:

        print(
            "Vector database not found. It will be created after document upload."
        )

    return store


@router.get("/")

def search(

    query: str

):

    return store.search(
        query
    )