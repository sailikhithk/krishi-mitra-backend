"""
Module for soil health-related CRUD operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.soil_health import SoilHealth
from app.schemas.soil_health import SoilHealthCreate, SoilHealthResponse


async def create_soil_health(
    session: AsyncSession, data: SoilHealthCreate
) -> SoilHealthResponse:
    """
    Create a new soil health record.

    Args:
        session (AsyncSession): The database session.
        data (SoilHealthCreate): The soil health data to create.

    Returns:
        SoilHealthResponse: The created soil health record.
    """
    soil_health = SoilHealth(**data.dict())
    session.add(soil_health)
    await session.commit()
    await session.refresh(soil_health)
    return soil_health


async def get_soil_health(
    session: AsyncSession, soil_health_id: int
) -> SoilHealthResponse:
    """
    Retrieve a soil health record by ID.

    Args:
        session (AsyncSession): The database session.
        soil_health_id (int): The ID of the soil health record to retrieve.

    Returns:
        SoilHealthResponse: The retrieved soil health record or None if not found.
    """
    result = await session.execute(
        select(SoilHealth).where(SoilHealth.id == soil_health_id)
    )
    soil_health = result.scalars().first()
    if not soil_health:
        return None
    return soil_health
