import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table, Enum, text
from datetime import datetime, timedelta
import random
from app.config import DATABASE_URL
from app.utils.auth import get_password_hash
import enum

# Create SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "AsyncSession" class
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create declarative base
Base = declarative_base()

class UserRole(enum.Enum):
    FARMER = "farmer"
    VENDOR = "vendor"
    ADMIN = "admin"

user_scheme = Table('user_scheme', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('scheme_id', Integer, ForeignKey('schemes.id'), primary_key=True)
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

async def truncate_tables():
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users, soil_health, bids, schemes, produce_listings, logistics, user_scheme CASCADE"))

async def insert_data():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Insert dummy users
            users = [
                User(id=1, username="john_doe", email="john@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.FARMER, farm_size=150.5, location="Anantapur"),
                User(id=2, username="jane_doe", email="jane@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.VENDOR, company_name="Jane's Agro", business_type="Wholesaler"),
                User(id=3, username="bob_smith", email="bob@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.FARMER, farm_size=200.0, location="Chittoor"),
                User(id=4, username="alice_johnson", email="alice@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.ADMIN, department="IT", access_level="Full")
            ]
            session.add_all(users)

            # Insert dummy soil health data
            soil_health_data = [
                SoilHealth(user_id=1, ph=6.5, nitrogen=0.3, phosphorus=0.2, potassium=0.5, organic_matter=1.2),
                SoilHealth(user_id=3, ph=6.8, nitrogen=0.35, phosphorus=0.25, potassium=0.55, organic_matter=1.4),
            ]
            session.add_all(soil_health_data)

            # Insert dummy produce listings
            crops = ["Wheat", "Corn", "Rice", "Soybeans", "Barley"]
            statuses = ["active", "completed", "cancelled"]
            produce_listings = [
                ProduceListing(
                    user_id=user_id,
                    crop=random.choice(crops),
                    quantity=round(random.uniform(100.0, 1000.0), 2),
                    base_price=round(random.uniform(50.0, 200.0), 2),
                    current_bid=round(random.uniform(50.0, 200.0), 2),
                    end_time=datetime.utcnow() + timedelta(days=random.randint(1, 7)),
                    status=random.choice(statuses),
                ) for user_id in [1, 3] for _ in range(5)
            ]
            session.add_all(produce_listings)

            # Insert dummy bids
            bid_statuses = ["pending", "accepted", "rejected"]
            bids = [
                Bid(
                    user_id=2,
                    produce_listing_id=listing.id,
                    quantity=round(random.uniform(50.0, listing.quantity), 2),
                    price=round(random.uniform(listing.base_price, listing.base_price * 1.5), 2),
                    status=random.choice(bid_statuses),
                ) for listing in produce_listings for _ in range(random.randint(1, 3))
            ]
            session.add_all(bids)

            # Insert dummy schemes
            schemes = [
                Scheme(name="Crop Insurance Scheme", description="Provides insurance coverage for crops", eligibility="All farmers", benefits="Financial protection against crop failure"),
                Scheme(name="Soil Health Card Scheme", description="Provides soil health assessment", eligibility="All farmers", benefits="Improved soil management"),
                Scheme(name="Kisan Credit Card", description="Provides credit for agricultural needs", eligibility="All farmers", benefits="Easy access to credit"),
                Scheme(name="Pradhan Mantri Fasal Bima Yojana", description="Crop insurance scheme", eligibility="All farmers", benefits="Comprehensive risk coverage")
            ]
            session.add_all(schemes)

            # Associate users with schemes
            for user in users:
                if user.role == UserRole.FARMER:
                    user.schemes = random.sample(schemes, random.randint(1, len(schemes)))

            # Insert dummy logistics data
            logistics_statuses = ["pending", "in_transit", "delivered", "cancelled"]
            logistics = [
                Logistics(
                    order_number=f"ORD-{random.randint(1000, 9999)}",
                    produce_listing_id=listing.id,
                    from_user_id=listing.user_id,
                    to_user_id=2,
                    status=random.choice(logistics_statuses),
                    expected_delivery=datetime.utcnow() + timedelta(days=random.randint(1, 14)),
                    actual_delivery=datetime.utcnow() + timedelta(days=random.randint(1, 14)) if random.choice([True, False]) else None,
                ) for listing in produce_listings if listing.status == "completed"
            ]
            session.add_all(logistics)

        await session.commit()

async def main():
    await truncate_tables()
    await insert_data()
    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    asyncio.run(main())