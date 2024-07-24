from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.database import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def read_users(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(**user.dict())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.get(User, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(existing_user, key, value)
    await session.commit()
    await session.refresh(existing_user)
    return existing_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"detail": "User deleted successfully"}
