from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.scheme import Scheme
from app.schemas.scheme import SchemeCreate, SchemeResponse
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=SchemeResponse)
async def create_scheme(data: SchemeCreate, session: AsyncSession = Depends(get_session)):
    scheme = Scheme(**data.dict())
    session.add(scheme)
    await session.commit()
    await session.refresh(scheme)
    return scheme

@router.get("/{scheme_id}", response_model=SchemeResponse)
async def get_scheme(scheme_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Scheme).where(Scheme.id == scheme_id))
    scheme = result.scalars().first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme
