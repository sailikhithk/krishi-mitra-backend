from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Logistics(Base):
    __tablename__ = 'logistics'

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True)
    produce_listing_id = Column(Integer, ForeignKey('produce_listings.id'))
    buyer_id = Column(Integer, ForeignKey('users.id'))
    farmer_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String)  # 'pending', 'in_transit', 'delivered', 'cancelled'
    expected_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    pickup_photo_url = Column(String)
    delivery_photo_url = Column(String)
    has_smartphone = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    produce_listing = relationship("ProduceListing", back_populates="logistics")
    buyer = relationship("User", foreign_keys=[buyer_id])
    farmer = relationship("User", foreign_keys=[farmer_id])
