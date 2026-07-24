"""
knowledge_service.py

Knowledge Base Service

Workflow

Upload
    ↓
Extract Text
    ↓
Chunk Text
    ↓
Generate Embeddings
    ↓
Store Metadata
"""

from backend.ai_engine.pipeline.knowledge_pipeline import KnowledgePipeline
from backend.models.uploaded_file import UploadedFile
from backend.models.knowledge import Knowledge
from backend.ai_engine.preprocessing.document_processor import DocumentExtractionError

class KnowledgeService:

    def __init__(self):

        self.pipeline = KnowledgePipeline()

        self.current_knowledge = None

    # --------------------------------------------------

    def build(

        self,

        file_path,

        file_id,

        db,
        subject_id

    ):

        # Run AI pipeline

        self.current_knowledge = self.pipeline.process(

            file_path

        )
        
        records = self.current_knowledge.get(

            "knowledge_records",

            []

        )

        saved = []

        total_chunks = len(records)

        for index, record in enumerate(records):


            if isinstance(record, dict):

                chunk_text = record.get(
                    "text",
                    ""
                )

            else:

                chunk_text = str(record)


            knowledge = Knowledge(

                file_id=file_id,

                subject_id=subject_id,

                content=chunk_text,

                embedding_id=f"faiss_{index}",

                vector_store="faiss",

                total_chunks=total_chunks,

                processed=True

            )

            db.add(knowledge)

            saved.append(knowledge)

        db.commit()

        

        return {

                "success": True,

                "documents": len(saved),

                "chunks": total_chunks,


                "message":
                    "Knowledge Base Created Successfully"

            }
        
    def build_knowledge_only(

        self,

        file_path,

        file_id,

        db,

        subject_id

    ):


        records = self.pipeline.process_without_generation(
            file_path
        )

        if not records:
            raise DocumentExtractionError(
                "No usable study content was found after preprocessing. Upload material with readable course content."
            )


        saved=[]


        total_chunks=len(records)


        for index, record in enumerate(records):
            if isinstance(record, dict):
                chunk_text = record.get("text", "")
            else:
                chunk_text = str(record)

            knowledge = Knowledge(

                file_id=file_id,

                subject_id=subject_id,

                content=chunk_text,

                embedding_id=f"faiss_{index}",

                vector_store="faiss",

                total_chunks=total_chunks,

                processed=True

            )


            db.add(knowledge)

            saved.append(knowledge)


        db.commit()

        # A material upload changes the subject corpus. Force the next
        # question-bank request to rebuild its FAISS index from every syllabus
        # and material record for this subject.
        self.current_knowledge = None


        return {

            "success":True,

            "chunks":total_chunks,

            "message":
            "Knowledge base created without AI generation"

        }    
    # --------------------------------------------------
    # --------------------------------------------------
# Build Subject Knowledge
# Used when uploading study material
# --------------------------------------------------


    def build_subject_knowledge(
        self,
        subject_id,
        db
    ):
        print("Building subject knowledge...")
        print(subject_id)
        knowledge_rows = (
            db.query(Knowledge)
            .filter(Knowledge.subject_id == subject_id)
            .all()
        )
        print("Knowledge rows:", len(knowledge_rows))
        if not knowledge_rows:
            raise Exception("No knowledge found for this subject.")

        records = []

        for row in knowledge_rows:

            records.append({
                "text": row.content
            })

        # -----------------------------------------
        # Rebuild FAISS index from stored knowledge
        # -----------------------------------------

        from backend.ai_engine.vector_store.faiss_manager import FAISSManager

        faiss_manager = FAISSManager()

        faiss_manager.build_index(records)
        print("FAISS chunks:",len(faiss_manager.get_all_chunks()))

        self.current_knowledge = {

            "knowledge_records": records,

            "faiss": faiss_manager,

            "metadata": {

                "subject_id": subject_id,

                "total_chunks": len(records)

            }

        }

        return {
            "success": True,
            "chunks": len(records),
            "faiss": faiss_manager,
            "knowledge_records": records,
            "message": "Subject knowledge built successfully"
        }
    
    def get(self):
        return self.current_knowledge

knowledge_service = KnowledgeService()
