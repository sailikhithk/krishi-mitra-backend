import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table, Enum, text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config import DATABASE_URL
import enum

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class UserRole(enum.Enum):
    FARMER = "farmer"
    VENDOR = "vendor"
    ADMIN = "admin"

user_scheme = Table('user_scheme', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('scheme_id', Integer, ForeignKey('schemes.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    farm_size = Column(Float)
    location = Column(String)
    company_name = Column(String)
    business_type = Column(String)
    department = Column(String)
    access_level = Column(String)
    soil_health = relationship("SoilHealth", back_populates="user")
    bids = relationship("Bid", back_populates="user")
    schemes = relationship("Scheme", secondary=user_scheme, back_populates="users")
    produce_listings = relationship("ProduceListing", back_populates="user")

class SoilHealth(Base):
    __tablename__ = 'soil_health'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ph = Column(Float)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    organic_matter = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="soil_health")

class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    produce_listing_id = Column(Integer, ForeignKey('produce_listings.id'))
    crop = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="bids")
    produce_listing = relationship("ProduceListing", back_populates="bids")

class Scheme(Base):
    __tablename__ = 'schemes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    eligibility = Column(String)
    benefits = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("User", secondary=user_scheme, back_populates="schemes")

class ProduceListing(Base):
    __tablename__ = 'produce_listings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    crop = Column(String)
    quantity = Column(Float)
    base_price = Column(Float)
    current_bid = Column(Float)
    end_time = Column(DateTime)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="produce_listings")
    bids = relationship("Bid", back_populates="produce_listing")
    logistics = relationship("Logistics", back_populates="produce_listing")

class Logistics(Base):
    __tablename__ = 'logistics'
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True)
    produce_listing_id = Column(Integer, ForeignKey('produce_listings.id'))
    from_user_id = Column(Integer, ForeignKey('users.id'))
    to_user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String)
    expected_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    produce_listing = relationship("ProduceListing", back_populates="logistics")
    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])

async def get_db_schema():
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public'
        """))
        return {(row.table_name, row.column_name): row.data_type for row in result}

def get_model_schema():
    model_schema = {}
    for model in [User, SoilHealth, Bid, Scheme, ProduceListing, Logistics]:
        for column in model.__table__.columns:
            model_schema[(model.__tablename__, column.name)] = str(column.type)
    return model_schema

async def compare_schemas():
    db_schema = await get_db_schema()
    model_schema = get_model_schema()

    print("Comparing database schemas...\n")
    
    for (table, column), type_ in model_schema.items():
        if (table, column) not in db_schema:
            print(f"Column {column} in table {table} is missing in the database.")
        elif db_schema[(table, column)] != type_:
            print(f"Column {column} in table {table} has different type. Expected: {type_}, Found: {db_schema[(table, column)]}")
    
    for (table, column) in db_schema:
        if (table, column) not in model_schema:
            print(f"Extra column {column} in table {table} found in the database.")

async def main():
    await compare_schemas()

if __name__ == "__main__":
    asyncio.run(main())