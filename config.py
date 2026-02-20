import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    CHROMA_PATH = os.path.join("data", "chroma_db")
    DATASET_NAME = "JDhruv14/Bhagavad-Gita_Dataset"

    # Local model (CPU) - Stable and No API costs
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # Stable 2026 model
    LLM_MODEL = "gemini-2.5-flash"