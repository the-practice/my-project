"""
Application configuration settings.
"""

import json
from pydantic_settings import BaseSettings
from pydantic import field_validator
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

    # CORS settings - defaults to localhost for development
    # Set via env var as: ALLOWED_ORIGINS=https://domain1.com,https://domain2.com (comma-separated)
    # Or: ALLOWED_ORIGINS=["https://domain1.com","https://domain2.com"] (JSON array)
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Database settings
    DATABASE_URL: str  # Required: must be provided via environment variable

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Anthropic API settings
    ANTHROPIC_API_KEY: str = ""  # Required for Vapi voice integration
    
    # Twilio settings
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Vapi.ai settings
    VAPI_API_KEY: str = ""
    VAPI_PHONE_NUMBER: str = ""
    
    # ElevenLabs settings
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = ""

    # Email settings
    IMAP_HOST: str = "imap.gmail.com"
    IMAP_PORT: int = 993
    IMAP_USERNAME: str = ""
    IMAP_PASSWORD: str = ""
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""

    # Extended voice settings
    TWILIO_WEBHOOK_URL: str = ""
    VAPI_BASE_URL: str = "https://api.vapi.ai"
    VAPI_PROJECT_ID: str = ""
    DEEPGRAM_API_KEY: str = ""

    # Security settings
    SECRET_KEY: str  # Required: must be provided via environment variable (use: openssl rand -hex 32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Task settings
    MAX_TASK_RETRIES: int = 3
    TASK_TIMEOUT_SECONDS: int = 300

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from env var as JSON array or comma-separated string."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v = v.strip()
            # If empty, return default localhost values
            if not v:
                return ["http://localhost:3000", "http://localhost:8000"]
            # Try parsing as JSON array first
            try:
                return json.loads(v)
            except (json.JSONDecodeError, ValueError):
                # Fall back to comma-separated format
                return [o.strip() for o in v.split(",") if o.strip()]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
