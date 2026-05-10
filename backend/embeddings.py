from sentence_transformers import SentenceTransformer
import os

class EmbeddingEngine:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, text_list):
        return self.model.encode(text_list).tolist()

embedding_engine = EmbeddingEngine()
