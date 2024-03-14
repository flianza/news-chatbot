import chromadb
from chromadb.config import Settings


def create_chroma_client():
    return chromadb.HttpClient(
        host="localhost",
        port=8500,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )
