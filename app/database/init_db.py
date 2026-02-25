"""
Database initialization.
"""

from app.database.session import engine, Base
from app.models import Task, TaskLog, User


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
