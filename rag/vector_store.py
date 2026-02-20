import os
import shutil
from langchain_chroma import Chroma
from config import Config
from rag.embedding import get_embedding_model


def create_vector_store(documents):
    """
    Initializes the ChromaDB using local HuggingFace embeddings.
    """
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(Config.CHROMA_PATH):
        shutil.rmtree(Config.CHROMA_PATH)
        print(f"Existing database at {Config.CHROMA_PATH} cleared.")

    print(f"Creating vector store at {Config.CHROMA_PATH}...")

    embeddings = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=Config.CHROMA_PATH
    )

    print("✅ Vector store created successfully!")
    return vectorstore


def get_vector_store():
    """
    Loads the existing vector store from the local directory.
    """
    embeddings = get_embedding_model()
    return Chroma(
        persist_directory=Config.CHROMA_PATH,
        embedding_function=embeddings
    )