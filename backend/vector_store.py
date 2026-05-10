from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./embeddings")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Ensure directory exists
os.makedirs(CHROMA_DB_PATH, exist_ok=True)


class VectorDBManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self._init_store()

    def _init_store(self):
        self.vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=self.embeddings,
            collection_name="medical_reports"
        )

    def add_texts(self, texts, metadatas=None):
        self.vector_store.add_texts(texts=texts, metadatas=metadatas)
        if hasattr(self.vector_store, "persist"):
            self.vector_store.persist()

    def get_retriever(self, k=3):
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    def clear_collection(self):
        """Reset the collection before a new PDF upload."""
        try:
            self.vector_store.delete_collection()
        except Exception:
            pass
        # Re-initialize so the store is usable again after clearing
        self._init_store()


vector_db_manager = VectorDBManager()
