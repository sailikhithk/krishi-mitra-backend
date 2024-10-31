from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.soil_health import SoilHealth
from app.schemas.soil_health import SoilHealthCreate
from app.schemas.soil_health import SoilHealthRead
from app.schemas.soil_health import SoilHealthUpdate

router = APIRouter()


@router.post("/", response_model=SoilHealthRead)
async def create_soil_health(
    soil_health: SoilHealthCreate, session: AsyncSession = Depends(get_async_session)
):
    new_soil_health = SoilHealth(**soil_health.dict())
    session.add(new_soil_health)
    await session.commit()
    await session.refresh(new_soil_health)
    return new_soil_health


@router.get("/{soil_health_id}", response_model=SoilHealthRead)
async def read_soil_health(
    soil_health_id: int, session: AsyncSession = Depends(get_async_session)
):
    soil_health = await session.get(SoilHealth, soil_health_id)
    if not soil_health:
        raise HTTPException(status_code=404, detail="Soil health record not found")
    return soil_health


@router.put("/{soil_health_id}", response_model=SoilHealthRead)
async def update_soil_health(
    soil_health_id: int,
    soil_health: SoilHealthUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    existing_soil_health = await session.get(SoilHealth, soil_health_id)
    if not existing_soil_health:
        raise HTTPException(status_code=404, detail="Soil health record not found")
    for key, value in soil_health.dict().items():
        setattr(existing_soil_health, key, value)
    await session.commit()
    await session.refresh(existing_soil_health)
    return existing_soil_health


@router.delete("/{soil_health_id}")
async def delete_soil_health(
    soil_health_id: int, session: AsyncSession = Depends(get_async_session)
):
    soil_health = await session.get(SoilHealth, soil_health_id)
    if not soil_health:
        raise HTTPException(status_code=404, detail="Soil health record not found")
    await session.delete(soil_health)
    await session.commit()
    return {"detail": "Soil health record deleted successfully"}
