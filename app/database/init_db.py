"""
Database initialization.
"""

import asyncio
import logging
from sqlalchemy import text
from app.database.session import engine, Base
from app.models import Task, TaskLog, User, Vault, SemanticMemory

logger = logging.getLogger(__name__)


def _init_db_sync():
    """Initialize database tables and required extensions synchronously."""
    # Create required PostgreSQL extensions
    with engine.connect() as conn:
        try:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
            logger.info("Created uuid-ossp extension")
        except Exception as e:
            logger.warning(f"Could not create uuid-ossp extension: {e}")

        try:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pgvector"'))
            logger.info("Created pgvector extension")
        except Exception as e:
            logger.warning(f"Could not create pgvector extension: {e}")

        conn.commit()

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


async def init_db():
    """Initialize database tables asynchronously."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _init_db_sync)
