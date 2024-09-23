import random
from datetime import datetime, timedelta

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.crud import user as user_crud
from app.schemas.user import UserCreate
from app.database import Base
from app.models.user import User, user_scheme
from app.models.soil_health import SoilHealth
from app.models.bid import Bid
from app.models.scheme import Scheme
from app.models.weather_data import WeatherData
from app.models.market_price import MarketPrice

# Create SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Remove all model class definitions from here

async def truncate_tables():
    """Truncates all database tables. This is used to reset the database when
    inserting dummy data.
    """
    async with async_session() as session:
        async with session.begin():
            tables = [User, SoilHealth, Bid, Scheme, WeatherData, MarketPrice]
            for table in tables:
                await session.execute(
                    text(f"TRUNCATE TABLE {table.__tablename__} CASCADE")
                )
            await session.execute(text("TRUNCATE TABLE user_scheme CASCADE"))
        await session.commit()

async def insert_data():
    async with async_session() as session:
        async with session.begin():
            try:
                # Insert dummy users
                users_data = [
                    {
                        "username": "john_doe",
                        "email": "john@example.com",
                        "password": "1234",  # Plain password
                    },
                    {
                        "username": "jane_doe",
                        "email": "jane@example.com",
                        "password": "1234",  # Plain password
                    },
                    {
                        "username": "bob_smith",
                        "email": "bob@example.com",
                        "password": "1234",  # Plain password
                    },
                    {
                        "username": "alice_johnson",
                        "email": "alice@example.com",
                        "password": "1234",  # Plain password
                    },
                ]
                
                created_users = []
                for user_data in users_data:
                    user_create = UserCreate(**user_data)
                    user = await user_crud.create_user(session, user_create)
                    created_users.append(user)

                # Insert dummy soil health data
                soil_health_data = [
                    {
                        "user_id": created_users[0].id,
                        "ph": 6.5,
                        "nitrogen": 0.3,
                        "phosphorus": 0.2,
                        "potassium": 0.5,
                        "organic_matter": 1.2,
                    },
                    # Add more soil health data for other users if needed
                ]
                await session.execute(insert(SoilHealth).values(soil_health_data))

                # Insert dummy bids
                crops = ["Wheat", "Corn", "Rice", "Soybeans", "Barley"]
                statuses = ["open", "closed", "pending", "accepted", "rejected"]
                bid_data = []
                for i in range(1, 21):  # Create 20 dummy bids
                    user = random.choice(created_users)
                    bid_data.append(
                        {
                            "id": i,
                            "user_id": user.id,
                            "crop": random.choice(crops),
                            "quantity": round(random.uniform(50.0, 500.0), 2),
                            "price": round(random.uniform(100.0, 1000.0), 2),
                            "status": random.choice(statuses),
                            "created_at": datetime.utcnow()
                            - timedelta(days=random.randint(0, 30)),
                        }
                    )
                await session.execute(insert(Bid).values(bid_data))

                # Insert dummy schemes
                await session.execute(
                    insert(Scheme).values(
                        [
                            {
                                "id": 1,
                                "name": "Crop Insurance Scheme",
                                "description": "Provides insurance coverage for crops",
                                "eligibility": "All farmers",
                                "benefits": "Financial protection against crop failure",
                            },
                            {
                                "id": 2,
                                "name": "Soil Health Card Scheme",
                                "description": "Provides soil health assessment",
                                "eligibility": "All farmers",
                                "benefits": "Improved soil management",
                            },
                            {
                                "id": 3,
                                "name": "Kisan Credit Card",
                                "description": "Provides credit for agricultural needs",
                                "eligibility": "All farmers",
                                "benefits": "Easy access to credit",
                            },
                            {
                                "id": 4,
                                "name": "Pradhan Mantri Fasal Bima Yojana",
                                "description": "Crop insurance scheme",
                                "eligibility": "All farmers",
                                "benefits": "Comprehensive risk coverage",
                            },
                        ]
                    )
                )

                # Associate users with schemes
                scheme_associations = []
                for user in created_users:
                    for scheme_id in range(1, 5):
                        if random.choice([True, False]):
                            scheme_associations.append(
                                {"user_id": user.id, "scheme_id": scheme_id}
                            )
                await session.execute(insert(user_scheme).values(scheme_associations))

                # Insert dummy weather data
                locations = ["New Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai"]
                weather_data = []
                for i in range(1, 21):  # Create 20 weather records
                    weather_data.append(
                        {
                            "id": i,
                            "location": random.choice(locations),
                            "temperature": round(random.uniform(20.0, 40.0), 1),
                            "humidity": round(random.uniform(30.0, 90.0), 1),
                            "precipitation": round(random.uniform(0.0, 50.0), 1),
                            "wind_speed": round(random.uniform(0.0, 30.0), 1),
                            "recorded_at": datetime.utcnow()
                            - timedelta(hours=random.randint(0, 72)),
                        }
                    )
                await session.execute(insert(WeatherData).values(weather_data))

                # Insert dummy market prices
                markets = [
                    "APMC Azadpur",
                    "Koyambedu Market",
                    "Vashi Market",
                    "Gultekdi Market",
                ]
                market_price_data = []
                for i in range(1, 31):  # Create 30 market price records
                    market_price_data.append(
                        {
                            "id": i,
                            "crop": random.choice(crops),
                            "price": round(random.uniform(50.0, 500.0), 2),
                            "market": random.choice(markets),
                            "recorded_at": datetime.utcnow()
                            - timedelta(days=random.randint(0, 30)),
                        }
                    )
                await session.execute(insert(MarketPrice).values(market_price_data))

            except Exception as e:
                print(f"An error occurred: {e}")
                raise

        # The commit will be handled automatically by the context manager

async def main():
    await truncate_tables()
    await insert_data()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
