from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.bid import Bid
from app.schemas.bid import BidCreate, BidResponse
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=BidResponse)
async def create_bid(data: BidCreate, session: AsyncSession = Depends(get_session)):
    bid = Bid(**data.dict())
    session.add(bid)
    await session.commit()
    await session.refresh(bid)
    return bid

@router.get("/{bid_id}", response_model=BidResponse)
async def get_bid(bid_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Bid).where(Bid.id == bid_id))
    bid = result.scalars().first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid
