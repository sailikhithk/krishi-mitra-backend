from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

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