from backend.ai_engine.pipeline.preprocessing_pipeline import PreprocessingPipeline
from backend.ai_engine.knowledge_base.knowledge_builder import KnowledgeBuilder
from backend.ai_engine.vector_store.faiss_manager import FAISSManager


class KnowledgePipeline:


    def __init__(self):

        self.preprocessing_pipeline = PreprocessingPipeline()

        self.knowledge_builder = KnowledgeBuilder()

        self.faiss_manager = FAISSManager()



    def process(self, file_path):


        print("\n========== STEP 1 ==========")
        print("Running preprocessing...")


        processed_document = self.preprocessing_pipeline.run(
            file_path
        )



        print("\n========== STEP 2 ==========")
        print("Creating knowledge chunks...")


        knowledge_records = self.knowledge_builder.build(
            processed_document
        )



        print("\n========== STEP 3 ==========")
        print("Creating FAISS index...")


        self.faiss_manager.build_index(
            knowledge_records
        )


        print("\nKnowledge Base Created")


        return {


            "processed_document": processed_document,


            "knowledge_records": knowledge_records,


            "faiss": self.faiss_manager,


            "metadata": {


                "document_name": file_path,


                "total_chunks":
                len(knowledge_records),


                "embedding_model":
                "all-MiniLM-L6-v2",


                "vector_database":
                "FAISS"

            }

        }



    def process_without_generation(self,file_path):


        processed_document = self.preprocessing_pipeline.run(
            file_path
        )


        knowledge_records = self.knowledge_builder.build(
            processed_document
        )

        print("==============================")
        print(
            "PIPELINE KNOWLEDGE RECORDS:",
            len(knowledge_records)
        )

        print(
            knowledge_records[:2]
        )

        print("==============================")
        return knowledge_records