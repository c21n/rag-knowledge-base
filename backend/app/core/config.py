"""Configuration settings for the application."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application
    APP_NAME: str = "RAG Knowledge Base API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # File upload settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "./uploads"
    
    # Allowed file types
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".md", ".txt"]
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost", "http://127.0.0.1:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Returns:
        Settings: Application settings.
    """
    return Settings()
