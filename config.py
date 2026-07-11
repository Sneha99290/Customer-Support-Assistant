from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHROMA_DB_COLLECTION_NAME = os.getenv("chroma_db_collection_name")

KNOWLEDGE_BASE_PATH = "./knowledge" 