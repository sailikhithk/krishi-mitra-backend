from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.logistics import Logistics
from app.schemas.logistics import LogisticsCreate
from app.schemas.logistics import LogisticsResponse
from app.schemas.logistics import LogisticsUpdate


async def create_logistics(
    session: AsyncSession, data: LogisticsCreate
) -> LogisticsResponse:
    logistics = Logistics(**data.dict())
    session.add(logistics)
    await session.commit()
    await session.refresh(logistics)
    return logistics


async def get_logistics(session: AsyncSession, logistics_id: int) -> LogisticsResponse:
    result = await session.execute(
        select(Logistics).where(Logistics.id == logistics_id)
    )
    logistics = result.scalars().first()
    return logistics


async def update_logistics(
    session: AsyncSession, logistics_id: int, data: LogisticsUpdate
) -> LogisticsResponse:
    result = await session.execute(
        select(Logistics).where(Logistics.id == logistics_id)
    )
    logistics = result.scalars().first()
    if logistics:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(logistics, key, value)
        await session.commit()
        await session.refresh(logistics)
    return logistics


async def delete_logistics(session: AsyncSession, logistics_id: int) -> bool:
    result = await session.execute(
        select(Logistics).where(Logistics.id == logistics_id)
    )
    logistics = result.scalars().first()
    if logistics:
        await session.delete(logistics)
        await session.commit()
        return True
    return False
