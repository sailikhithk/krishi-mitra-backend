import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)


def inspect_db():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Current tables in the database:")
    for table_name in tables:
        print(f"Table: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(f"  Column: {column['name']}, Type: {column['type']}")


if __name__ == "__main__":
    inspect_db()
