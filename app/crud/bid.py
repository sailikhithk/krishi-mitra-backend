from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.bid import Bid
from app.schemas.bid import BidCreate, BidResponse, BidUpdate

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
    result = await session.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalars().first()
    if not bid:
        return None
    return bid

async def update_bid(session: AsyncSession, bid_id: int, data: BidUpdate) -> BidResponse:
    """
    Update an existing bid in the database.

    Args:
        session (AsyncSession): The database session.
        bid_id (int): The ID of the bid to update.
        data (BidUpdate): The updated bid data.

    Returns:
        BidResponse: The updated bid.
    """
    result = await session.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalars().first()
    if bid:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(bid, key, value)
        await session.commit()
        await session.refresh(bid)
    return bid

async def delete_bid(session: AsyncSession, bid_id: int) -> bool:
    """
    Delete a bid from the database.

    Args:
        session (AsyncSession): The database session.
        bid_id (int): The ID of the bid to delete.

    Returns:
        bool: True if the bid was deleted, False otherwise.
    """
    result = await session.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalars().first()
    if bid:
        await session.delete(bid)
        await session.commit()
        return True
    return False