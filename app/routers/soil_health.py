from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.database import get_async_session
from app.models.soil_health import SoilHealth
from app.schemas.soil_health import SoilHealthCreate, SoilHealthRead, SoilHealthUpdate

router = APIRouter()


@router.get("/", response_model=List[SoilHealthRead])
async def read_soil_health(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a list of soil health records.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        session (AsyncSession): The database session.

    Returns:
        List[SoilHealthRead]: A list of soil health records.
    """
    result = await session.execute(select(SoilHealth).offset(skip).limit(limit))
    soil_healths = result.scalars().all()
    return soil_healths


@router.post("/", response_model=SoilHealthRead)
async def create_soil_health(
    soil_health: SoilHealthCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new soil health record.

    Args:
        soil_health (SoilHealthCreate): The soil health data to create.
        session (AsyncSession): The database session.

    Returns:
        SoilHealthRead: The created soil health record.
    """
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
