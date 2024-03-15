import os

OLLAMA_URL = os.getenv("OLLAMA_URL", None)

CHROMA_DB_SERVER = os.getenv("CHROMA_DB_SERVER", "localhost")
CHROMA_DB_PORT = int(os.getenv("CHROMA_DB_PORT", "8000"))
CHROMA_DB_COLLECTION = os.getenv("CHROMA_DB_COLLECTION", "news")

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")
CHAT_MODEL = os.getenv("CHAT_MODEL")
