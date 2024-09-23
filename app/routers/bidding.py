"""
Module for bidding-related routes.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_async_session
from app.models.bid import Bid
from app.schemas.bid import BidCreate, BidRead, BidUpdate

router = APIRouter()


@router.get("/", response_model=List[BidRead])
async def read_bids(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a list of bids.

    Args:
        skip (int): Number of bids to skip.
        limit (int): Maximum number of bids to return.
        session (AsyncSession): The database session.

    Returns:
        List[BidRead]: A list of bids.
    """
    result = await session.execute(select(Bid).offset(skip).limit(limit))
    bids = result.scalars().all()
    return bids


@router.post("/", response_model=BidRead)
async def create_bid(
    bid: BidCreate, session: AsyncSession = Depends(get_async_session)
):
    new_bid = Bid(**bid.dict())
    session.add(new_bid)
    await session.commit()
    await session.refresh(new_bid)
    return new_bid


@router.get("/{bid_id}", response_model=BidRead)
async def read_bid(bid_id: int, session: AsyncSession = Depends(get_async_session)):
    bid = await session.get(Bid, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid


@router.put("/{bid_id}", response_model=BidRead)
async def update_bid(
    bid_id: int, bid: BidUpdate, session: AsyncSession = Depends(get_async_session)
):
    existing_bid = await session.get(Bid, bid_id)
    if not existing_bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    for key, value in bid.dict().items():
        setattr(existing_bid, key, value)
    await session.commit()
    await session.refresh(existing_bid)
    return existing_bid


@router.delete("/{bid_id}")
async def delete_bid(bid_id: int, session: AsyncSession = Depends(get_async_session)):
    bid = await session.get(Bid, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    await session.delete(bid)
    await session.commit()
    return {"detail": "Bid deleted successfully"}
