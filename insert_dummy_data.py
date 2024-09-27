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
    role = Column(String, nullable=False)  # Changed from Enum(UserRole) to String
    created_at = Column(DateTime, default=datetime.utcnow)
    soil_health = relationship("SoilHealth", back_populates="user")
    bids = relationship("Bid", back_populates="user")
    schemes = relationship("Scheme", secondary=user_scheme, back_populates="users")

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
    crop = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="bids")

class Scheme(Base):
    __tablename__ = 'schemes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    eligibility = Column(String)
    benefits = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("User", secondary=user_scheme, back_populates="schemes")

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class MarketPrice(Base):
    __tablename__ = 'market_prices'
    id = Column(Integer, primary_key=True, index=True)
    crop = Column(String, index=True)
    price = Column(Float)
    market = Column(String)
    recorded_at = Column(DateTime, default=datetime.utcnow)

async def truncate_tables():
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users, soil_health, bids, schemes, weather_data, market_prices, user_scheme CASCADE"))

async def insert_data():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Insert dummy users
            users = [
                User(id=1, username="john_doe", email="john@example.com", hashed_password=get_password_hash("1234"), role=UserRole.FARMER.value),
                User(id=2, username="jane_doe", email="jane@example.com", hashed_password=get_password_hash("1234"), role=UserRole.VENDOR.value),
                User(id=3, username="bob_smith", email="bob@example.com", hashed_password=get_password_hash("1234"), role=UserRole.FARMER.value),
                User(id=4, username="alice_johnson", email="alice@example.com", hashed_password=get_password_hash("1234"), role=UserRole.ADMIN.value)
            ]
            session.add_all(users)

            # Insert dummy soil health data
            soil_health_data = [
                SoilHealth(user_id=1, ph=6.5, nitrogen=0.3, phosphorus=0.2, potassium=0.5, organic_matter=1.2),
                SoilHealth(user_id=2, ph=7.0, nitrogen=0.4, phosphorus=0.3, potassium=0.6, organic_matter=1.3),
                SoilHealth(user_id=3, ph=6.8, nitrogen=0.35, phosphorus=0.25, potassium=0.55, organic_matter=1.4),
                SoilHealth(user_id=4, ph=7.2, nitrogen=0.45, phosphorus=0.35, potassium=0.65, organic_matter=1.5)
            ]
            session.add_all(soil_health_data)

            # Insert dummy bids
            crops = ["Wheat", "Corn", "Rice", "Soybeans", "Barley"]
            statuses = ["open", "closed", "pending", "accepted", "rejected"]
            bids = [
                Bid(
                    user_id=random.randint(1, 4),
                    crop=random.choice(crops),
                    quantity=round(random.uniform(50.0, 500.0), 2),
                    price=round(random.uniform(100.0, 1000.0), 2),
                    status=random.choice(statuses),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                ) for _ in range(20)
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
                user.schemes = random.sample(schemes, random.randint(1, len(schemes)))

            # Insert dummy weather data
            locations = ["New Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai"]
            weather_data = [
                WeatherData(
                    location=random.choice(locations),
                    temperature=round(random.uniform(20.0, 40.0), 1),
                    humidity=round(random.uniform(30.0, 90.0), 1),
                    precipitation=round(random.uniform(0.0, 50.0), 1),
                    wind_speed=round(random.uniform(0.0, 30.0), 1),
                    recorded_at=datetime.utcnow() - timedelta(hours=random.randint(0, 72))
                ) for _ in range(20)
            ]
            session.add_all(weather_data)

            # Insert dummy market prices
            markets = ["APMC Azadpur", "Koyambedu Market", "Vashi Market", "Gultekdi Market"]
            market_prices = [
                MarketPrice(
                    crop=random.choice(crops),
                    price=round(random.uniform(50.0, 500.0), 2),
                    market=random.choice(markets),
                    recorded_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                ) for _ in range(30)
            ]
            session.add_all(market_prices)

        await session.commit()

async def main():
    await truncate_tables()
    await insert_data()
    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    asyncio.run(main())