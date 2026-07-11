from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from config import EMBEDDING_MODEL, CHROMA_DB_COLLECTION_NAME, KNOWLEDGE_BASE_PATH
import os
import uuid

class IngestionService:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name=CHROMA_DB_COLLECTION_NAME)

    def load_pdf(self, folder_path):

        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                yield from documents

    def split_documents(self, documents, chunk_size=1000, chunk_overlap=200):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_documents(documents)
    
    def create_embeddings(self, chunks):
        embeddings = self.embedding_model.encode([chunk.page_content for chunk in chunks])
        return embeddings
    
    def vector_db_store(self,chunks,embeddings):
        ids = []
        documents = []
        embedding_vectors = []
        metadatas = []
        for chunk, embedding_vector in zip(chunks, embeddings):
            ids.append(str(uuid.uuid4()))
            documents.append(chunk.page_content)
            metadata = dict(chunk.metadata) if hasattr(chunk, 'metadata') else {}
            metadata['content_length'] = len(chunk.page_content)
            metadatas.append(metadata)
            try:
                embedding_vectors.append(embedding_vector.tolist())
            except AttributeError:
                embedding_vectors.append(list(embedding_vector))
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embedding_vectors,
            metadatas=metadatas
        )

    def ingestion_pipeline(self,folder_path):
        documents = list(self.load_pdf(folder_path))
        chunks = self.split_documents(documents)
        embeddings = self.create_embeddings(chunks)
        self.vector_db_store(chunks, embeddings)
        print(f"Successfully indexed {len(chunks)} chunks.")

if __name__ == "__main__":
    ingestion_service = IngestionService()
    ingestion_service.ingestion_pipeline(folder_path=KNOWLEDGE_BASE_PATH)
