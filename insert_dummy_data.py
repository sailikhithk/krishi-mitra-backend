import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random
from app.config import DATABASE_URL
from app.utils.auth import get_password_hash
from create_db import engine, Base, User, SoilHealth, Scheme, Bid, ProduceListing, Payment, Logistics, UserRole, ProduceCategory, user_scheme

# Create a configured "AsyncSession" class
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def insert_data():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Insert dummy users
            users = [
                    User(username="john_farmer", email="john@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.FARMER, farm_size=150.5, location="Anantapur", phone_number="+911234567890", aadhar_card_url="http://example.com/aadhar/john.jpg"),
                    User(username="jane_buyer", email="jane@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.BUYER, company_name="Jane's Agro", business_type="Wholesaler", phone_number="+919876543210", aadhar_card_url="http://example.com/aadhar/jane.jpg"),
                    User(username="bob_farmer", email="bob@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.FARMER, farm_size=200.0, location="Chittoor", phone_number="+917890123456", aadhar_card_url="http://example.com/aadhar/bob.jpg"),
                    User(username="alice_admin", email="alice@krishimitra.com", hashed_password=get_password_hash("1234"), role=UserRole.ADMIN, department="IT", access_level="Full", phone_number="+915678901234", aadhar_card_url="http://example.com/aadhar/alice.jpg")
                ]
            session.add_all(users)
            await session.flush()

            # Insert dummy soil health data
            soil_health_data = [
                SoilHealth(user_id=users[0].id, ph=6.5, nitrogen=0.3, phosphorus=0.2, potassium=0.5, organic_matter=1.2),
                SoilHealth(user_id=users[2].id, ph=6.8, nitrogen=0.35, phosphorus=0.25, potassium=0.55, organic_matter=1.4),
            ]
            session.add_all(soil_health_data)

            # Insert dummy produce listings
            crops = ["Wheat", "Corn", "Rice", "Soybeans", "Barley"]
            statuses = ["active", "completed", "cancelled"]
            produce_listings = [
                ProduceListing(
                    user_id=user.id,
                    crop=random.choice(crops),
                    category=random.choice(list(ProduceCategory)),
                    quantity=round(random.uniform(100.0, 1000.0), 2),
                    base_price=round(random.uniform(50.0, 200.0), 2),
                    minimum_bid_price=round(random.uniform(40.0, 180.0), 2),
                    current_bid=round(random.uniform(50.0, 200.0), 2),
                    govt_price=round(random.uniform(45.0, 190.0), 2),
                    end_time=datetime.utcnow() + timedelta(days=random.randint(1, 7)),
                    status=random.choice(statuses),
                    photo_urls=f"http://example.com/photo{random.randint(1,5)}.jpg",
                    description=f"High-quality {random.choice(crops)} from {random.choice(['Anantapur', 'Chittoor'])}",
                    pickup_location=random.choice(["Farm Gate", "Local Mandi", "Warehouse"]),
                    distance=round(random.uniform(5.0, 50.0), 1)
                ) for user in users if user.role == UserRole.FARMER for _ in range(3)
            ]
            session.add_all(produce_listings)
            await session.flush()

            # Insert dummy bids
            bid_statuses = ["pending", "accepted", "rejected"]
            bids = [
                Bid(
                    user_id=users[1].id,
                    produce_listing_id=listing.id,
                    crop=listing.crop,
                    quantity=round(random.uniform(50.0, listing.quantity), 2),
                    price=round(random.uniform(listing.base_price, listing.base_price * 1.5), 2),
                    status=random.choice(bid_statuses),
                    acceptance_status=random.choice(["accepted", "rejected", "pending"]),
                    rejection_reason="Price too low" if random.choice([True, False]) else None,
                    delivery_address=f"{random.randint(1, 100)} Main St, City"
                ) for listing in produce_listings for _ in range(random.randint(1, 3))
            ]
            session.add_all(bids)
            await session.flush()

            # Insert dummy payments
            payment_statuses = ["pending", "completed", "failed"]
            payments = [
                Payment(
                    bid_id=bid.id,
                    amount=bid.price * bid.quantity,
                    upi_transaction_id=f"UPI{random.randint(100000, 999999)}",
                    status=random.choice(payment_statuses)
                ) for bid in bids if bid.status == "accepted"
            ]
            session.add_all(payments)

            # Insert dummy schemes
            schemes = [
                Scheme(name="Crop Insurance Scheme", description="Provides insurance coverage for crops", eligibility="All farmers", benefits="Financial protection against crop failure"),
                Scheme(name="Soil Health Card Scheme", description="Provides soil health assessment", eligibility="All farmers", benefits="Improved soil management"),
            ]
            session.add_all(schemes)
            await session.flush()

            # Associate users with schemes
            for user in users:
                if user.role == UserRole.FARMER:
                    user_schemes = random.sample(schemes, random.randint(1, len(schemes)))
                    for scheme in user_schemes:
                        await session.execute(user_scheme.insert().values(user_id=user.id, scheme_id=scheme.id))

            # Insert dummy logistics data
            logistics_statuses = ["pending", "in_transit", "delivered", "cancelled"]
            logistics = [
                Logistics(
                    order_number=f"ORD-{random.randint(1000, 9999)}",
                    produce_listing_id=listing.id,
                    from_user_id=listing.user_id,
                    to_user_id=users[1].id,
                    status=random.choice(logistics_statuses),
                    expected_delivery=datetime.utcnow() + timedelta(days=random.randint(1, 14)),
                    actual_delivery=datetime.utcnow() + timedelta(days=random.randint(1, 14)) if random.choice([True, False]) else None,
                    pickup_photo_url=f"http://example.com/pickup{random.randint(1,5)}.jpg",
                    delivery_photo_url=f"http://example.com/delivery{random.randint(1,5)}.jpg",
                    has_smartphone=random.choice([True, False])
                ) for listing in produce_listings if listing.status == "completed"
            ]
            session.add_all(logistics)

        await session.commit()

async def main():
    await insert_data()
    print("Dummy data inserted successfully.")

if __name__ == "__main__":
    asyncio.run(main())
