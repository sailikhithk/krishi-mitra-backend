from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, index=True)
    bid_id = Column(Integer, ForeignKey('bids.id'))
    amount = Column(Float)
    upi_transaction_id = Column(String)
    status = Column(String)  # 'pending', 'completed', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bid = relationship("Bid", back_populates="payment")
