"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field, UUID4, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime


# ── Task Schemas ──────────────────────────────────────────────────────────────

class CreateTaskRequest(BaseModel):
    """Request model for creating a new task."""
    goal: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="What the task should accomplish"
    )
    user_id: str = Field(
        ...,
        description="ID of the user creating the task (UUID string)"
    )
    metadata_json: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional metadata for the task"
    )


class TaskResponse(BaseModel):
    """Response model for task details."""
    id: str
    user_id: str
    goal: str
    state: str
    metadata_json: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TaskLogResponse(BaseModel):
    """Response model for task log entries."""
    id: str
    event_type: str
    payload_json: Dict[str, Any]
    timestamp: Optional[str] = None


class TaskActionResponse(BaseModel):
    """Response model for task action endpoints (create, execute, replan)."""
    status: str
    task_id: str
    message: str


# ── Voice Schemas ─────────────────────────────────────────────────────────────

class VapiWebhookRequest(BaseModel):
    """Request model for Vapi.ai webhook events."""
    model_config = ConfigDict(extra="allow")  # Vapi may send undocumented fields

    type: str = Field(
        ...,
        description="Vapi event type (assistant-request, function-call, end-of-call-report, status-update, etc.)"
    )
    # Optional top-level fields that appear in various event types
    status: Optional[str] = None
    endedReason: Optional[str] = None
    transcript: Optional[str] = None
    duration: Optional[float] = None
    function: Optional[Dict[str, Any]] = None


# ── Email Schemas ─────────────────────────────────────────────────────────────

class EmailWebhookRequest(BaseModel):
    """Request model for email webhook events from various providers."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    # Support multiple provider field names via aliases
    # "from" is a Python keyword so we use from_ with alias
    from_: Optional[str] = Field(None, alias="from")
    sender: Optional[str] = None
    From: Optional[str] = None  # Capitalized variant (some providers)
    subject: Optional[str] = None
    Subject: Optional[str] = None
    text: Optional[str] = None
    plain: Optional[str] = None
    body: Optional[str] = Field(None, alias="body-plain")
    body_plain: Optional[str] = None


class EmailWebhookResponse(BaseModel):
    """Response model for email webhook."""
    status: str
    from_addr: Optional[str] = None
    subject: Optional[str] = None
    message: str


class InboxResponse(BaseModel):
    """Response model for inbox polling."""
    status: str
    count: int
    emails: List[Dict[str, Any]] = []
    message: Optional[str] = None
