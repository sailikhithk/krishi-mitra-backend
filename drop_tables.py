import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))
    print("All tables dropped successfully.")


async def main():
    await drop_all_tables()


if __name__ == "__main__":
    asyncio.run(main())
