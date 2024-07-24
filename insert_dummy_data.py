from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Session
session = SessionLocal()

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

def insert_dummy_data():
    # Insert dummy users
    user1 = User(username="john_doe", email="john@example.com", hashed_password="hashed_password1")
    user2 = User(username="jane_doe", email="jane@example.com", hashed_password="hashed_password2")
    session.add_all([user1, user2])
    session.commit()

    # Insert dummy soil health data
    soil_health1 = SoilHealth(user_id=user1.id, ph=6.5, nitrogen=0.3, phosphorus=0.2, potassium=0.5, organic_matter=1.2)
    soil_health2 = SoilHealth(user_id=user2.id, ph=7.0, nitrogen=0.4, phosphorus=0.3, potassium=0.6, organic_matter=1.3)
    session.add_all([soil_health1, soil_health2])
    session.commit()

    # Insert dummy bids
    bid1 = Bid(user_id=user1.id, crop="Wheat", quantity=100.0, price=200.0, status="open")
    bid2 = Bid(user_id=user2.id, crop="Corn", quantity=150.0, price=250.0, status="closed")
    session.add_all([bid1, bid2])
    session.commit()

    # Insert dummy schemes
    scheme1 = Scheme(name="Scheme A", description="Description A", eligibility="Eligibility A", benefits="Benefits A")
    scheme2 = Scheme(name="Scheme B", description="Description B", eligibility="Eligibility B", benefits="Benefits B")
    session.add_all([scheme1, scheme2])
    session.commit()

    # Associate users with schemes
    user1.schemes.append(scheme1)
    user2.schemes.append(scheme2)
    session.commit()

    # Insert dummy weather data
    weather1 = WeatherData(location="Location A", temperature=25.5, humidity=60.0, precipitation=5.0, wind_speed=10.0)
    weather2 = WeatherData(location="Location B", temperature=22.0, humidity=55.0, precipitation=10.0, wind_speed=15.0)
    session.add_all([weather1, weather2])
    session.commit()

    # Insert dummy market prices
    market_price1 = MarketPrice(crop="Wheat", price=200.0, market="Market A")
    market_price2 = MarketPrice(crop="Corn", price=250.0, market="Market B")
    session.add_all([market_price1, market_price2])
    session.commit()

    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    insert_dummy_data()
    session.close()
