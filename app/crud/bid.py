"""
Module for bid-related CRUD operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.bid import Bid
from app.schemas.bid import BidCreate, BidResponse


async def create_bid(session: AsyncSession, data: BidCreate) -> BidResponse:
    """
    Create a new bid in the database.

    Args:
        session (AsyncSession): The database session.
        data (BidCreate): The bid data to create.

    Returns:
        BidResponse: The created bid.
    """
    bid = Bid(**data.dict())
    session.add(bid)
    await session.commit()
    await session.refresh(bid)
    return bid


async def get_bid(session: AsyncSession, bid_id: int) -> BidResponse:
    """
    Retrieve a bid by ID.

    Args:
        session (AsyncSession): The database session.
        bid_id (int): The ID of the bid to retrieve.

    Returns:
        BidResponse: The retrieved bid or None if not found.
    """
    result = await session.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalars().first()
    if not bid:
        return None
    return bid
