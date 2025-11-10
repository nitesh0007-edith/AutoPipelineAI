"""
Configuration Management - Load and manage application configuration
"""
import os
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    INPUT_DIR = BASE_DIR / os.getenv("INPUT_DIR", "input_docs")
    OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "data/processed")
    REPORTS_DIR = BASE_DIR / os.getenv("REPORTS_DIR", "data/reports")
    EXPORTS_DIR = BASE_DIR / os.getenv("EXPORTS_DIR", "data/exports")
    CACHE_DIR = BASE_DIR / os.getenv("CACHE_DIR", "data/cache")
    LOG_DIR = BASE_DIR / os.getenv("LOG_DIR", "logs")

    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
    OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3")

    # Database Configuration
    DUCKDB_PATH = str(BASE_DIR / os.getenv("DUCKDB_PATH", "data/database.duckdb"))
    SQLITE_PATH = str(BASE_DIR / os.getenv("SQLITE_PATH", "data/database.db"))

    # Cache Configuration
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_ROTATION = os.getenv("LOG_ROTATION", "1 MB")

    # Memory Store Configuration
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "100"))

    # PDF Extraction Configuration
    EXTRACTED_IMAGES_DIR = BASE_DIR / os.getenv("EXTRACTED_IMAGES_DIR", "data/extracted_images")
    EXTRACTED_TABLES_DIR = BASE_DIR / os.getenv("EXTRACTED_TABLES_DIR", "data/extracted")

    # SpaCy Model
    SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")

    # Security Settings
    ALLOWED_MODULES = os.getenv(
        "ALLOWED_MODULES",
        "pandas,numpy,plotly,matplotlib,seaborn,datetime,json,re,math,statistics"
    ).split(",")

    # Performance Settings
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.INPUT_DIR,
            cls.OUTPUT_DIR,
            cls.REPORTS_DIR,
            cls.EXPORTS_DIR,
            cls.CACHE_DIR,
            cls.LOG_DIR,
            cls.EXTRACTED_IMAGES_DIR,
            cls.EXTRACTED_TABLES_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info("Created necessary directories")

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return getattr(cls, key, default)

    @classmethod
    def display(cls) -> dict:
        """
        Get all configuration as dictionary

        Returns:
            Configuration dictionary
        """
        config_dict = {}

        for key in dir(cls):
            if key.isupper() and not key.startswith("_"):
                value = getattr(cls, key)
                # Don't expose sensitive information
                if "KEY" in key or "PASSWORD" in key:
                    config_dict[key] = "***"
                else:
                    config_dict[key] = str(value)

        return config_dict


# Initialize directories on import
try:
    Config.ensure_directories()
except Exception as e:
    logger.warning(f"Failed to create directories: {e}")
