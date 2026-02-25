"""
Task, Vault, and SemanticMemory models aligned with schema.sql.
"""

import uuid
import enum
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database.session import Base


class TaskState(str, enum.Enum):
    """Task state enum matching schema.sql states."""
    INIT = "INIT"
    GATHER_INFO = "GATHER_INFO"
    RESEARCH = "RESEARCH"
    READY_TO_EXECUTE = "READY_TO_EXECUTE"
    CALL_IN_PROGRESS = "CALL_IN_PROGRESS"
    AWAITING_USER_INPUT = "AWAITING_USER_INPUT"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class User(Base):
    """User model matching schema.sql users table."""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    tasks = relationship("Task", back_populates="creator")
    vault_entries = relationship("Vault", back_populates="user")
    semantic_memories = relationship("SemanticMemory", back_populates="user")


class Task(Base):
    """Task model matching schema.sql tasks table."""
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal = Column(Text, nullable=False)
    state = Column(String(50), default="INIT", nullable=False, index=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")
    creator = relationship("User", back_populates="tasks")


class TaskLog(Base):
    """Task log model matching schema.sql task_logs table."""
    __tablename__ = "task_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    payload_json = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Relationships
    task = relationship("Task", back_populates="logs")


class Vault(Base):
    """Vault model for storing encrypted credentials matching schema.sql vault table."""
    __tablename__ = "vault"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company = Column(String(255), nullable=False)
    account_number = Column(String(100), nullable=False)
    pin = Column(String(50), nullable=False)  # AES-256 encrypted
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    user = relationship("User", back_populates="vault_entries")


class SemanticMemory(Base):
    """Semantic memory model for vector embeddings matching schema.sql semantic_memory table."""
    __tablename__ = "semantic_memory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=True)  # OpenAI embedding dimension
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="semantic_memories")
