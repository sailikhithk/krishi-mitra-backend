from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.scheme import Scheme
from app.schemas.scheme import SchemeCreate
from app.schemas.scheme import SchemeResponse


async def create_scheme(session: AsyncSession, data: SchemeCreate) -> SchemeResponse:
    scheme = Scheme(**data.dict())
    session.add(scheme)
    await session.commit()
    await session.refresh(scheme)
    return scheme


async def get_scheme(session: AsyncSession, scheme_id: int) -> SchemeResponse:
    result = await session.execute(select(Scheme).where(Scheme.id == scheme_id))
    scheme = result.scalars().first()
    if not scheme:
        return None
    return scheme
