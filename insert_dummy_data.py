from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table, text
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
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
                {'id': 2, 'username': "jane_doe", 'email': "jane@example.com", 'hashed_password': "hashed_password2"}
            ]))

            # Insert dummy soil health data
            await session.execute(insert(SoilHealth).values([
                {'id': 1, 'user_id': 1, 'ph': 6.5, 'nitrogen': 0.3, 'phosphorus': 0.2, 'potassium': 0.5, 'organic_matter': 1.2},
                {'id': 2, 'user_id': 2, 'ph': 7.0, 'nitrogen': 0.4, 'phosphorus': 0.3, 'potassium': 0.6, 'organic_matter': 1.3}
            ]))

            # Insert dummy bids
            await session.execute(insert(Bid).values([
                {'id': 1, 'user_id': 1, 'crop': "Wheat", 'quantity': 100.0, 'price': 200.0, 'status': "open"},
                {'id': 2, 'user_id': 2, 'crop': "Corn", 'quantity': 150.0, 'price': 250.0, 'status': "closed"}
            ]))

            # Insert dummy schemes
            await session.execute(insert(Scheme).values([
                {'id': 1, 'name': "Scheme A", 'description': "Description A", 'eligibility': "Eligibility A", 'benefits': "Benefits A"},
                {'id': 2, 'name': "Scheme B", 'description': "Description B", 'eligibility': "Eligibility B", 'benefits': "Benefits B"}
            ]))

            # Associate users with schemes
            await session.execute(insert(user_scheme).values([
                {'user_id': 1, 'scheme_id': 1},
                {'user_id': 2, 'scheme_id': 2}
            ]))

            # Insert dummy weather data
            await session.execute(insert(WeatherData).values([
                {'id': 1, 'location': "Location A", 'temperature': 25.5, 'humidity': 60.0, 'precipitation': 5.0, 'wind_speed': 10.0},
                {'id': 2, 'location': "Location B", 'temperature': 22.0, 'humidity': 55.0, 'precipitation': 10.0, 'wind_speed': 15.0}
            ]))

            # Insert dummy market prices
            await session.execute(insert(MarketPrice).values([
                {'id': 1, 'crop': "Wheat", 'price': 200.0, 'market': "Market A"},
                {'id': 2, 'crop': "Corn", 'price': 250.0, 'market': "Market B"}
            ]))

        await session.commit()

async def main():
    await truncate_tables()
    await insert_data()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
