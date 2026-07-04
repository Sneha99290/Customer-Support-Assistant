from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, CHROMA_DB_COLLECTION_NAME
import chromadb

class Retriever:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name=CHROMA_DB_COLLECTION_NAME)

    def retrieve(self, query, top_k=5):
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results