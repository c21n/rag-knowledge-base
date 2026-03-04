"""Configuration management for the RAG Knowledge Base API."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # OpenAI API Configuration (supports Alibaba Bailian)
    OPENAI_API_KEY: str = "your_openai_api_key_here"
    OPENAI_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-v1"

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./data/app.db"

    # ChromaDB Configuration
    CHROMA_PERSIST_DIR: str = "./data/chroma"

    # File Upload Configuration
    UPLOAD_DIR: str = "./data/uploads"

    # Embedding Model Configuration
    EMBEDDING_MODEL: str = "text-embedding-ada-002"

    # Text Chunking Configuration
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings with environment variable values.
    """
    return Settings()
