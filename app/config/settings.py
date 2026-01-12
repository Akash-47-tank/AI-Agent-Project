"""
Application Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Paths
    DOCUMENTS_DIR: str = "data/documents"
    INDEX_PATH: str = "data/faiss_index.bin"
    DOCUMENTS_PATH: str = "data/documents.pkl"
    LOG_DIR: str = "logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()