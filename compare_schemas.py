import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

from app.models import Bid, MarketPrice, Scheme, SoilHealth, User, WeatherData

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# Reflect the current database schema
current_metadata = MetaData()
current_metadata.reflect(bind=engine)

# Define the declarative base for the models
Base = declarative_base()

# List of model classes
model_classes = [User, SoilHealth, Bid, Scheme, WeatherData, MarketPrice]

# Create a metadata object from the models
model_metadata = MetaData()
for model_class in model_classes:
    model_class.metadata.create_all(bind=engine)
    model_metadata.tables.update(model_class.metadata.tables)


def compare_schemas():
    print("Comparing database schemas...\n")
    for table_name in model_metadata.tables:
        if table_name not in current_metadata.tables:
            print(f"Table {table_name} is missing in the current database.")
        else:
            model_table = model_metadata.tables[table_name]
            current_table = current_metadata.tables[table_name]
            model_columns = set(model_table.columns.keys())
            current_columns = set(current_table.columns.keys())

            for column in model_columns - current_columns:
                print(
                    f"Column {column} in table {table_name} is missing in the current database."
                )
            for column in current_columns - model_columns:
                print(
                    f"Column {column} in table {table_name} is extra in the current database."
                )
            for column in model_columns & current_columns:
                if str(model_table.columns[column].type) != str(
                    current_table.columns[column].type
                ):
                    print(
                        f"Column {column} in table {table_name} has different type. Expected: {model_table.columns[column].type}, Found: {current_table.columns[column].type}"
                    )


if __name__ == "__main__":
    compare_schemas()
