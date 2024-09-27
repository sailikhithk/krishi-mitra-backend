import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL)

async def inspect_db():
    async with engine.begin() as conn:
        # Get table names
        result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]

        print("Current tables in the database:")
        for table_name in tables:
            print(f"Table: {table_name}")
            
            # Get column information
            result = await conn.execute(text(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
            """))
            columns = result.fetchall()
            
            for column in columns:
                print(f"  Column: {column[0]}, Type: {column[1]}")

async def main():
    await inspect_db()

if __name__ == "__main__":
    asyncio.run(main())