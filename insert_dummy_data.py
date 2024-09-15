from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table, text
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timedelta
import random
from app.config import DATABASE_URL

# Create SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Create declarative base
Base = declarative_base()

# Define association table for many-to-many relationship between User and Scheme
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
    """Truncates all database tables. This is used to reset the database when
    inserting dummy data.
    """
    async with async_session() as session:
        async with session.begin():
            tables = [User, SoilHealth, Bid, Scheme, WeatherData, MarketPrice]
            for table in tables:
                await session.execute(text(f'TRUNCATE TABLE {table.__table__.name} CASCADE'))
            await session.execute(text('TRUNCATE TABLE user_scheme CASCADE'))
        await session.commit()

async def insert_data():
    async with async_session() as session:
        async with session.begin():
            # Insert dummy users
            await session.execute(insert(User).values([
                {'id': 1, 'username': "john_doe", 'email': "john@example.com", 'hashed_password': "hashed_password1"},
                {'id': 2, 'username': "jane_doe", 'email': "jane@example.com", 'hashed_password': "hashed_password2"},
                {'id': 3, 'username': "bob_smith", 'email': "bob@example.com", 'hashed_password': "hashed_password3"},
                {'id': 4, 'username': "alice_johnson", 'email': "alice@example.com", 'hashed_password': "hashed_password4"}
            ]))

            # Insert dummy soil health data
            await session.execute(insert(SoilHealth).values([
                {'id': 1, 'user_id': 1, 'ph': 6.5, 'nitrogen': 0.3, 'phosphorus': 0.2, 'potassium': 0.5, 'organic_matter': 1.2},
                {'id': 2, 'user_id': 2, 'ph': 7.0, 'nitrogen': 0.4, 'phosphorus': 0.3, 'potassium': 0.6, 'organic_matter': 1.3},
                {'id': 3, 'user_id': 3, 'ph': 6.8, 'nitrogen': 0.35, 'phosphorus': 0.25, 'potassium': 0.55, 'organic_matter': 1.4},
                {'id': 4, 'user_id': 4, 'ph': 7.2, 'nitrogen': 0.45, 'phosphorus': 0.35, 'potassium': 0.65, 'organic_matter': 1.5}
            ]))

            # Insert dummy bids
            crops = ["Wheat", "Corn", "Rice", "Soybeans", "Barley"]
            statuses = ["open", "closed", "pending", "accepted", "rejected"]
            bid_data = []
            for i in range(1, 21):  # Create 20 dummy bids
                bid_data.append({
                    'id': i,
                    'user_id': random.randint(1, 4),
                    'crop': random.choice(crops),
                    'quantity': round(random.uniform(50.0, 500.0), 2),
                    'price': round(random.uniform(100.0, 1000.0), 2),
                    'status': random.choice(statuses),
                    'created_at': datetime.utcnow() - timedelta(days=random.randint(0, 30))
                })
            await session.execute(insert(Bid).values(bid_data))

            # Insert dummy schemes
            await session.execute(insert(Scheme).values([
                {'id': 1, 'name': "Crop Insurance Scheme", 'description': "Provides insurance coverage for crops", 'eligibility': "All farmers", 'benefits': "Financial protection against crop failure"},
                {'id': 2, 'name': "Soil Health Card Scheme", 'description': "Provides soil health assessment", 'eligibility': "All farmers", 'benefits': "Improved soil management"},
                {'id': 3, 'name': "Kisan Credit Card", 'description': "Provides credit for agricultural needs", 'eligibility': "All farmers", 'benefits': "Easy access to credit"},
                {'id': 4, 'name': "Pradhan Mantri Fasal Bima Yojana", 'description': "Crop insurance scheme", 'eligibility': "All farmers", 'benefits': "Comprehensive risk coverage"}
            ]))

            # Associate users with schemes
            scheme_associations = []
            for user_id in range(1, 5):
                for scheme_id in range(1, 5):
                    if random.choice([True, False]):
                        scheme_associations.append({'user_id': user_id, 'scheme_id': scheme_id})
            await session.execute(insert(user_scheme).values(scheme_associations))

            # Insert dummy weather data
            locations = ["New Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai"]
            weather_data = []
            for i in range(1, 21):  # Create 20 weather records
                weather_data.append({
                    'id': i,
                    'location': random.choice(locations),
                    'temperature': round(random.uniform(20.0, 40.0), 1),
                    'humidity': round(random.uniform(30.0, 90.0), 1),
                    'precipitation': round(random.uniform(0.0, 50.0), 1),
                    'wind_speed': round(random.uniform(0.0, 30.0), 1),
                    'recorded_at': datetime.utcnow() - timedelta(hours=random.randint(0, 72))
                })
            await session.execute(insert(WeatherData).values(weather_data))

            # Insert dummy market prices
            markets = ["APMC Azadpur", "Koyambedu Market", "Vashi Market", "Gultekdi Market"]
            market_price_data = []
            for i in range(1, 31):  # Create 30 market price records
                market_price_data.append({
                    'id': i,
                    'crop': random.choice(crops),
                    'price': round(random.uniform(50.0, 500.0), 2),
                    'market': random.choice(markets),
                    'recorded_at': datetime.utcnow() - timedelta(days=random.randint(0, 30))
                })
            await session.execute(insert(MarketPrice).values(market_price_data))

        await session.commit()

async def main():
    await truncate_tables()
    await insert_data()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
