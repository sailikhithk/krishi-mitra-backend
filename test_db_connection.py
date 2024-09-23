import asyncio
from app.database import get_async_session
from app.models.user import User
from sqlalchemy.future import select

async def test_db_connection():
    async for session in get_async_session():
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            print(f"Connected to the database. Found {len(users)} users.")
        except Exception as e:
print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    asyncio.run(test_db_connection())