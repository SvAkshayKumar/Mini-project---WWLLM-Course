import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "IndicWrite AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "3000"))

    # Vector Database & Embeddings (Local FAISS CPU)
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "storage/faiss/index.faiss")
    FAISS_METADATA_PATH: str = os.getenv("FAISS_METADATA_PATH", "storage/faiss/metadata.json")
    DOCUMENTS_DIR: str = os.getenv("DOCUMENTS_DIR", "storage/documents")
    UPLOADS_DIR: str = os.getenv("UPLOADS_DIR", "storage/uploads")
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # AI4Bharat & BharatGen Endpoints (Optional external endpoints)
    AI4BHARAT_INDICXLIT_ENDPOINT: Optional[str] = os.getenv("AI4BHARAT_INDICXLIT_ENDPOINT", None)
    AI4BHARAT_INDICTRANS2_ENDPOINT: Optional[str] = os.getenv("AI4BHARAT_INDICTRANS2_ENDPOINT", None)
    BHARATGEN_API_KEY: Optional[str] = os.getenv("BHARATGEN_API_KEY", None)
    BHARATGEN_MODEL_ENDPOINT: Optional[str] = os.getenv("BHARATGEN_MODEL_ENDPOINT", None)

    # Gemini Supporting LLM
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
