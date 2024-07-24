from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.soil_health import SoilHealth
from app.schemas.soil_health import SoilHealthCreate, SoilHealthResponse
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=SoilHealthResponse)
async def create_soil_health(data: SoilHealthCreate, session: AsyncSession = Depends(get_session)):
    soil_health = SoilHealth(**data.dict())
    session.add(soil_health)
    await session.commit()
    await session.refresh(soil_health)
    return soil_health

@router.get("/{soil_health_id}", response_model=SoilHealthResponse)
async def get_soil_health(soil_health_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SoilHealth).where(SoilHealth.id == soil_health_id))
    soil_health = result.scalars().first()
    if not soil_health:
        raise HTTPException(status_code=404, detail="Soil health not found")
    return soil_health
