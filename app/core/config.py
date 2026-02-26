"""
Application configuration settings.
"""

import json
from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
from typing import List
from typing_extensions import Self


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
    ALLOWED_ORIGINS_RAW: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        validation_alias="ALLOWED_ORIGINS"
    )
    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)
    
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

    @model_validator(mode="after")
    def parse_allowed_origins(self) -> Self:
        """Parse ALLOWED_ORIGINS_RAW from env var as JSON array or comma-separated string."""
        v = self.ALLOWED_ORIGINS_RAW.strip()
        # If empty, use default localhost values
        if not v:
            self.ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]
        else:
            # Try parsing as JSON array first
            try:
                self.ALLOWED_ORIGINS = json.loads(v)
            except (json.JSONDecodeError, ValueError):
                # Fall back to comma-separated format
                self.ALLOWED_ORIGINS = [o.strip() for o in v.split(",") if o.strip()]
        return self

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
