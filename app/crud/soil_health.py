from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.soil_health import SoilHealth
from app.schemas.soil_health import SoilHealthCreate
from app.schemas.soil_health import SoilHealthResponse


async def create_soil_health(
    session: AsyncSession, data: SoilHealthCreate
) -> SoilHealthResponse:
    soil_health = SoilHealth(**data.dict())
    session.add(soil_health)
    await session.commit()
    await session.refresh(soil_health)
    return soil_health


async def get_soil_health(
    session: AsyncSession, soil_health_id: int
) -> SoilHealthResponse:
    result = await session.execute(
        select(SoilHealth).where(SoilHealth.id == soil_health_id)
    )
    soil_health = result.scalars().first()
    if not soil_health:
        return None
    return soil_health
