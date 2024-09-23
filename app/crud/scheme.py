"""
Module for scheme-related CRUD operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.scheme import Scheme
from app.schemas.scheme import SchemeCreate, SchemeResponse


async def create_scheme(session: AsyncSession, data: SchemeCreate) -> SchemeResponse:
    """
    Create a new scheme in the database.

    Args:
        session (AsyncSession): The database session.
        data (SchemeCreate): The scheme data to create.

    Returns:
        SchemeResponse: The created scheme.
    """
    scheme = Scheme(**data.dict())
    session.add(scheme)
    await session.commit()
    await session.refresh(scheme)
    return scheme


async def get_scheme(session: AsyncSession, scheme_id: int) -> SchemeResponse:
    """
    Retrieve a scheme by ID.

    Args:
        session (AsyncSession): The database session.
        scheme_id (int): The ID of the scheme to retrieve.

    Returns:
        SchemeResponse: The retrieved scheme or None if not found.
    """
    result = await session.execute(select(Scheme).where(Scheme.id == scheme_id))
    scheme = result.scalars().first()
    if not scheme:
        return None
    return scheme
