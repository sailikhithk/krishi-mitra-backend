import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table, Enum
from datetime import datetime
from app.config import DATABASE_URL
import enum

# Create SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create declarative base
Base = declarative_base()

class UserRole(enum.Enum):
    FARMER = "farmer"
    VENDOR = "vendor"
    ADMIN = "admin"

# Define association table for many-to-many relationship between User and Scheme
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
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Farmer specific fields
    farm_size = Column(Float)
    location = Column(String)
    
    # Vendor specific fields
    company_name = Column(String)
    business_type = Column(String)
    
    # Admin specific fields
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
    status = Column(String)  # 'active', 'completed', 'cancelled'
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
    status = Column(String)  # 'pending', 'in_transit', 'delivered', 'cancelled'
    expected_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    produce_listing = relationship("ProduceListing", back_populates="logistics")
    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

async def main():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main())