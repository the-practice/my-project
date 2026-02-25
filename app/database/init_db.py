"""
Database initialization.
"""

import asyncio
from app.database.session import engine, Base
from app.models import Task, TaskLog, User, Vault, SemanticMemory


def _init_db_sync():
    """Initialize database tables synchronously."""
    Base.metadata.create_all(bind=engine)


async def init_db():
    """Initialize database tables asynchronously."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _init_db_sync)
