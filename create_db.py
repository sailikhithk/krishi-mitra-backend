from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

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

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    create_tables()