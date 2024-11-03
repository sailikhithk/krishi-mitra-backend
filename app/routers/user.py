from datetime import timedelta
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_async_session
from app.models.user import User
from app.models.user import UserRole
from app.schemas.scheme import SchemeRead
from app.schemas.user import Token
from app.schemas.user import UserCreate
from app.schemas.user import UserProfileUpdate
from app.schemas.user import UserRead
from app.schemas.user import UserUpdate
from app.utils.auth import authenticate_user
from app.utils.auth import create_access_token
from app.utils.auth import get_current_user
from app.utils.auth import get_password_hash

router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def signup(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    # Check if user already exists
    result = await session.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Validate the role
    if user.role not in [role.value for role in UserRole]:
        raise HTTPException(status_code=400, detail="Invalid user role")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,  # Store the role as a string
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    print(
        f"User {new_user.username} created with hashed password: {new_user.hashed_password}"
    )
    return new_user


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    print(
        f"Attempting login for user: {form_data.username}"
    )
    # First find the user to get their role
    result = await session.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    print(f"User {user.username} logged in successfully, token generated.")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
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
async def update_user(
    user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_async_session)
):
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


@router.put("/me/profile", response_model=UserRead)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    for key, value in profile_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    await session.commit()
    await session.refresh(current_user)
    return current_user


@router.get("/me/schemes", response_model=List[SchemeRead])
async def get_user_schemes(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await session.refresh(current_user, attribute_names=["schemes"])
    return current_user.schemes
