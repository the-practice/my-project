"""
Application configuration settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # Project settings
    PROJECT_NAME: str = "Autonomous AI Operator"
    PROJECT_DESCRIPTION: str = "A production-ready, multi-channel AI operator that autonomously executes real-world tasks through voice, email, and web research."
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/autonomous_ai_operator"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Anthropic API settings
    ANTHROPIC_API_KEY: str = ""
    
    # Twilio settings
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Vapi.ai settings
    VAPI_API_KEY: str = ""
    VAPI_PHONE_NUMBER: str = ""
    
    # ElevenLabs settings
    ELEVENLABS_API_KEY: str = ""
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Task settings
    MAX_TASK_RETRIES: int = 3
    TASK_TIMEOUT_SECONDS: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
