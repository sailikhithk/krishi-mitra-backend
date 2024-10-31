from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.database import Base


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    produce_listing_id = Column(Integer, ForeignKey("produce_listings.id"))
    crop = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    status = Column(String)
    acceptance_status = Column(String)
    rejection_reason = Column(String)
    delivery_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="bids")
    produce_listing = relationship("ProduceListing", back_populates="bids")
    payment = relationship("Payment", back_populates="bid", uselist=False)
