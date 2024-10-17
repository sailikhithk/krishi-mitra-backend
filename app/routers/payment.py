from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate
from app.utils.auth import get_current_user
from app.models.user import User, UserRole
from typing import List

router = APIRouter()

@router.post("/", response_model=PaymentRead)
async def create_payment(
    payment: PaymentCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user.role != UserRole.BUYER:
        raise HTTPException(status_code=403, detail="Only buyers can create payments")
    new_payment = Payment(**payment.dict())
    session.add(new_payment)
    await session.commit()
    await session.refresh(new_payment)
    return new_payment

@router.get("/", response_model=List[PaymentRead])
async def read_payments(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user.role == UserRole.BUYER:
        result = await session.execute(select(Payment).join(Payment.bid).where(Payment.bid.user_id == current_user.id).offset(skip).limit(limit))
    elif current_user.role == UserRole.FARMER:
        result = await session.execute(select(Payment).join(Payment.bid).join(Payment.bid.produce_listing).where(Payment.bid.produce_listing.farmer_id == current_user.id).offset(skip).limit(limit))
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view payments")
    payments = result.scalars().all()
    return payments

@router.get("/{payment_id}", response_model=PaymentRead)
async def read_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    payment = await session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if current_user.role == UserRole.BUYER and payment.bid.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this payment")
    if current_user.role == UserRole.FARMER and payment.bid.produce_listing.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this payment")
    return payment

@router.put("/{payment_id}", response_model=PaymentRead)
async def update_payment(
    payment_id: int,
    payment: PaymentUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    existing_payment = await session.get(Payment, payment_id)
    if not existing_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can update payments")
    for key, value in payment.dict(exclude_unset=True).items():
        setattr(existing_payment, key, value)
    await session.commit()
    await session.refresh(existing_payment)
    return existing_payment

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    payment = await session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete payments")
    await session.delete(payment)
    await session.commit()