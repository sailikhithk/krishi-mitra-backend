"""
Database configuration and models.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import DATABASE_URL

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Create declarative base
Base = declarative_base()

# Dependency
async def get_async_session() -> AsyncSession:
    """
    Dependency to get the async session.

    Yields:
        AsyncSession: The database session.
    """
    try:
        async with AsyncSessionLocal() as session:
            logger.debug("Database connection successful")
            yield session
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise
