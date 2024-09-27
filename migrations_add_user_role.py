import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.models.user import User, UserRole
from app.config import DATABASE_URL

# Create SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL)

# Create a configured "AsyncSession" class
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def add_role_column():
    async with engine.begin() as conn:
        # Add the role column
        await conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(255)'))
    
    # Set a default role for existing users
    async with AsyncSessionLocal() as session:
        try:
            await session.execute(text("UPDATE users SET role = :role WHERE role IS NULL"), {'role': UserRole.FARMER.value})
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Error setting default role: {e}")
            return

    async with engine.begin() as conn:
        # Change the column to non-nullable
        await conn.execute(text('ALTER TABLE users ALTER COLUMN role SET NOT NULL'))

    print("Migration completed successfully.")

async def main():
    await add_role_column()

if __name__ == "__main__":
    asyncio.run(main())