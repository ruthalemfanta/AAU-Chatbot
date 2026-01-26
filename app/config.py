"""Configuration management for AAU Helpdesk Chatbot."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Model Paths
    MODEL_DIR: Path = Path("models")
    INTENT_MODEL_PATH: Optional[Path] = None
    NER_MODEL_PATH: Optional[Path] = None
    VECTORIZER_PATH: Optional[Path] = None
    
    # Data Paths
    DATA_DIR: Path = Path("data")
    RAW_DATA_PATH: Path = Path("data/raw/collected_data.csv")
    PROCESSED_DATA_PATH: Path = Path("data/processed/cleaned_data.csv")
    ANNOTATED_DATA_DIR: Path = Path("data/annotated")
    KNOWLEDGE_BASE_DIR: Path = Path("data/knowledge_base")
    
    # Config Paths
    CONFIG_DIR: Path = Path("config")
    INTENT_CONFIG_PATH: Path = Path("config/intent.yaml")
    
    # Logging
    LOG_LEVEL: str = "INFO"


# Global settings instance
settings = Settings()
