from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate, Token
from app.database import get_async_session
from app.utils.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from datetime import timedelta

router = APIRouter()

@router.post("/signup", response_model=UserRead)
async def signup(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    # Check if user already exists
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    print(f"Signing up user: {user.username} with password: {user.hashed_password}")
    hashed_password = get_password_hash(user.hashed_password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    print(f"User {new_user.username} created with hashed password: {new_user.hashed_password}")
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    print(f"Logging in user: {form_data.username} with password: {form_data.password}")
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print(f"User {user.username} logged in successfully, token generated.")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserRead])
async def read_users(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

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
