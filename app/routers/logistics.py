from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
from app.models.logistics import Logistics
from app.schemas.logistics import LogisticsCreate, LogisticsRead, LogisticsUpdate
from app.utils.auth import get_current_user
from app.models.user import User, UserRole
from typing import List

router = APIRouter()

@router.post("/", response_model=LogisticsRead)
async def create_logistics(
    logistics: LogisticsCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user.role not in [UserRole.FARMER, UserRole.BUYER]:
        raise HTTPException(status_code=403, detail="Not authorized to create logistics")
    new_logistics = Logistics(**logistics.dict())
    session.add(new_logistics)
    await session.commit()
    await session.refresh(new_logistics)
    return new_logistics

@router.get("/", response_model=List[LogisticsRead])
async def read_logistics(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Logistics)
        .where((Logistics.from_user_id == current_user.id) | (Logistics.to_user_id == current_user.id))
        .offset(skip)
        .limit(limit)
    )
    logistics = result.scalars().all()
    return logistics

@router.get("/{logistics_id}", response_model=LogisticsRead)
async def read_logistics_by_id(
    logistics_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    logistics = await session.get(Logistics, logistics_id)
    if not logistics:
        raise HTTPException(status_code=404, detail="Logistics not found")
    if current_user.id not in [logistics.from_user_id, logistics.to_user_id]:
        raise HTTPException(status_code=403, detail="Not authorized to view this logistics")
    return logistics

@router.put("/{logistics_id}", response_model=LogisticsRead)
async def update_logistics(
    logistics_id: int,
    logistics: LogisticsUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    existing_logistics = await session.get(Logistics, logistics_id)
    if not existing_logistics:
        raise HTTPException(status_code=404, detail="Logistics not found")
    if current_user.id not in [existing_logistics.from_user_id, existing_logistics.to_user_id]:
        raise HTTPException(status_code=403, detail="Not authorized to update this logistics")
    for key, value in logistics.dict(exclude_unset=True).items():
        setattr(existing_logistics, key, value)
    await session.commit()
    await session.refresh(existing_logistics)
    return existing_logistics

@router.delete("/{logistics_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_logistics(
    logistics_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    logistics = await session.get(Logistics, logistics_id)
    if not logistics:
        raise HTTPException(status_code=404, detail="Logistics not found")
    if current_user.id not in [logistics.from_user_id, logistics.to_user_id]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this logistics")
    await session.delete(logistics)
    await session.commit()