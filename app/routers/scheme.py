from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_async_session
from app.models.scheme import Scheme
from app.schemas.scheme import SchemeCreate, SchemeRead, SchemeUpdate

router = APIRouter()


@router.get("/", response_model=List[SchemeRead])
async def read_schemes(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a list of schemes.

    Args:
        skip (int): Number of schemes to skip.
        limit (int): Maximum number of schemes to return.
        session (AsyncSession): The database session.

    Returns:
        List[SchemeRead]: A list of schemes.
    """
    result = await session.execute(select(Scheme).offset(skip).limit(limit))
    schemes = result.scalars().all()
    return schemes


@router.post("/", response_model=SchemeRead)
async def create_scheme(
    scheme: SchemeCreate, session: AsyncSession = Depends(get_async_session)
):
    new_scheme = Scheme(**scheme.dict())
    session.add(new_scheme)
    await session.commit()
    await session.refresh(new_scheme)
    return new_scheme


@router.get("/{scheme_id}", response_model=SchemeRead)
async def read_scheme(
    scheme_id: int, session: AsyncSession = Depends(get_async_session)
):
    scheme = await session.get(Scheme, scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme


@router.put("/{scheme_id}", response_model=SchemeRead)
async def update_scheme(
    scheme_id: int,
    scheme: SchemeUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    existing_scheme = await session.get(Scheme, scheme_id)
    if not existing_scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    for key, value in scheme.dict().items():
        setattr(existing_scheme, key, value)
    await session.commit()
    await session.refresh(existing_scheme)
    return existing_scheme


@router.delete("/{scheme_id}")
async def delete_scheme(
    scheme_id: int, session: AsyncSession = Depends(get_async_session)
):
    scheme = await session.get(Scheme, scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    await session.delete(scheme)
    await session.commit()
    return {"detail": "Scheme deleted successfully"}
