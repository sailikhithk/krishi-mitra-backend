from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
from app.models.bid import Bid
from app.models.produce_listing import ProduceListing
from app.schemas.bid import BidCreate, BidRead, BidUpdate
from app.utils.auth import get_current_user
from app.models.user import User, UserRole
from typing import List

router = APIRouter()

@router.get("/", response_model=List[BidRead])
async def read_bids(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user.role == UserRole.FARMER:
        result = await session.execute(select(Bid).join(ProduceListing).where(ProduceListing.farmer_id == current_user.id).offset(skip).limit(limit))
    elif current_user.role == UserRole.BUYER:
        result = await session.execute(select(Bid).where(Bid.user_id == current_user.id).offset(skip).limit(limit))
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view bids")
    bids = result.scalars().all()
    return bids

@router.post("/", response_model=BidRead)
async def create_bid(
    bid: BidCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user.role != UserRole.BUYER:
        raise HTTPException(status_code=403, detail="Only buyers can create bids")
    new_bid = Bid(**bid.dict(), user_id=current_user.id)
    session.add(new_bid)
    await session.commit()
    await session.refresh(new_bid)
    return new_bid

@router.get("/{bid_id}", response_model=BidRead)
async def read_bid(
    bid_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    bid = await session.get(Bid, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if current_user.role == UserRole.BUYER and bid.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this bid")
    if current_user.role == UserRole.FARMER and bid.produce_listing.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this bid")
    return bid

@router.put("/{bid_id}", response_model=BidRead)
async def update_bid(
    bid_id: int,
    bid: BidUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    existing_bid = await session.get(Bid, bid_id)
    if not existing_bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if existing_bid.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this bid")
    for key, value in bid.dict(exclude_unset=True).items():
        setattr(existing_bid, key, value)
    await session.commit()
    await session.refresh(existing_bid)
    return existing_bid

@router.delete("/{bid_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bid(
    bid_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    bid = await session.get(Bid, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if bid.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this bid")
    await session.delete(bid)
    await session.commit()