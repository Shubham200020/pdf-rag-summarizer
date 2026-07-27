import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
TEMP_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "temp_uploads")

os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)
