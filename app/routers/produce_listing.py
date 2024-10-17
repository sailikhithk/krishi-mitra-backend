from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
from app.models.produce_listing import ProduceListing
from app.schemas.produce_listing import ProduceListingCreate, ProduceListingRead, ProduceListingUpdate
from app.utils.auth import get_current_user
from app.models.user import User, UserRole
from typing import List

router = APIRouter()

@router.post("/", response_model=ProduceListingRead)
async def create_produce_listing(
    produce_listing: ProduceListingCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user.role != UserRole.FARMER:
        raise HTTPException(status_code=403, detail="Only farmers can create produce listings")
    
    new_produce_listing = ProduceListing(**produce_listing.dict(), user_id=current_user.id, farmer_id=current_user.id, status="active")
    session.add(new_produce_listing)
    await session.commit()
    await session.refresh(new_produce_listing)
    return new_produce_listing

@router.get("/", response_model=List[ProduceListingRead])
async def read_produce_listings(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(ProduceListing).offset(skip).limit(limit))
    listings = result.scalars().all()
    return listings

@router.get("/{listing_id}", response_model=ProduceListingRead)
async def read_produce_listing(
    listing_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    listing = await session.get(ProduceListing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Produce listing not found")
    return listing

@router.put("/{listing_id}", response_model=ProduceListingRead)
async def update_produce_listing(
    listing_id: int,
    produce_listing: ProduceListingUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    existing_listing = await session.get(ProduceListing, listing_id)
    if not existing_listing:
        raise HTTPException(status_code=404, detail="Produce listing not found")
    if existing_listing.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own listings")
    
    for key, value in produce_listing.dict(exclude_unset=True).items():
        setattr(existing_listing, key, value)
    
    await session.commit()
    await session.refresh(existing_listing)
    return existing_listing

@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_produce_listing(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    listing = await session.get(ProduceListing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Produce listing not found")
    if listing.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own listings")
    
    await session.delete(listing)
    await session.commit()