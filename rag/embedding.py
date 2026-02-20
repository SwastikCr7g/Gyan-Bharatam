from langchain_huggingface import HuggingFaceEmbeddings
from config import Config


def get_embedding_model():
    """
    Initializes local HuggingFace embeddings.
    This runs on your local machine and avoids API 404 errors.
    """
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}

    return HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )