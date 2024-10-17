from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class ProduceCategory(enum.Enum):
    DAILY = "daily"
    WEEKLY_MONTHLY = "weekly_monthly"
    DRY_SPICES_NUTS = "dry_spices_nuts"
    GRAINS = "grains"

class ProduceListing(Base):
    __tablename__ = 'produce_listings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    crop = Column(String)
    category = Column(Enum(ProduceCategory), nullable=False)
    quantity = Column(Float)
    base_price = Column(Float)
    minimum_bid_price = Column(Float)
    current_bid = Column(Float)
    govt_price = Column(Float)
    end_time = Column(DateTime)
    status = Column(String)  # 'active', 'completed', 'cancelled'
    photo_urls = Column(String)  # Store as comma-separated URLs
    description = Column(String)
    pickup_location = Column(String)
    distance = Column(Float)  # Distance for delivery in km
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="produce_listings")
    bids = relationship("Bid", back_populates="produce_listing")
    logistics = relationship("Logistics", back_populates="produce_listing")
    farmer_id = Column(Integer, ForeignKey('users.id'))
    farmer = relationship("User", foreign_keys=[farmer_id], back_populates="farmer_produce_listings")