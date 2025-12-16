import os
from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_embeddings")
    embedding_dimension: int = int(os.getenv("EMBEDDING_DIMENSION", "1536"))

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2048"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Neon Postgres Configuration
    neon_host: str = os.getenv("NEON_HOST", "")
    neon_database: str = os.getenv("NEON_DATABASE", "")
    neon_username: str = os.getenv("NEON_USERNAME", "")
    neon_password: str = os.getenv("NEON_PASSWORD", "")
    neon_port: int = int(os.getenv("NEON_PORT", "5432"))

    # Application Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Validation
    def validate_config(self) -> bool:
        """
        Validate that all required configuration values are present.
        """
        required_fields = [
            self.qdrant_url,
            self.qdrant_api_key,
            self.openai_api_key,
            self.neon_host,
            self.neon_database,
            self.neon_username,
            self.neon_password,
        ]

        for field in required_fields:
            if not field:
                return False
        return True

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global settings instance
settings = Settings()

# Validate configuration on startup
if not settings.validate_config():
    raise ValueError("Missing required environment variables. Please check your .env file.")