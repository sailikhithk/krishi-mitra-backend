"""
Module for user-related CRUD operations.
"""

import logging

logger = logging.getLogger(__name__)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils.auth import get_password_hash

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


async def create_user(session: AsyncSession, data: UserCreate) -> UserResponse:
    """
    Create a new user in the database.

    Args:
        session (AsyncSession): The database session.
        data (UserCreate): The user data to create.

    Returns:
        UserResponse: The created user.
    """
    logger.debug(f"Creating user: {data.username}")
    hashed_password = get_password_hash(data.password)
    user = User(**data.dict(exclude={"password"}), hashed_password=hashed_password)
    session.add(user)
    try:
        await session.flush()
        await session.refresh(user)
        logger.info(f"User created successfully: {user.username}")
        return user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise


async def get_user(session: AsyncSession, user_id: int) -> UserResponse:
    """
    Retrieve a user by ID.

    Args:
        session (AsyncSession): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserResponse: The retrieved user or None if not found.
    """
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None  # Ensure this matches the expected return type
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    """
    Retrieve a user by username.

    Args:
        session (AsyncSession): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        User: The retrieved user or None if not found.
    """
    logger.debug(f"Getting user by username: {username}")
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user:
        logger.info(f"User found: {username}")
    else:
        logger.warning(f"User not found: {username}")
    return user
