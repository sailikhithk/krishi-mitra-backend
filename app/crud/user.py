from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from utils.auth import get_password_hash

async def create_user(session: AsyncSession, data: UserCreate) -> UserResponse:
    hashed_password = get_password_hash(data.hashed_password)
    user = User(**data.dict(), hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user(session: AsyncSession, user_id: int) -> UserResponse:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None
    return user
