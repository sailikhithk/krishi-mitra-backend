from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    FARMER = "farmer"
    VENDOR = "vendor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Farmer specific fields
    farm_size = Column(Float)
    location = Column(String)
    
    # Vendor specific fields
    company_name = Column(String)
    business_type = Column(String)
    
    # Admin specific fields
    department = Column(String)
    access_level = Column(String)

    soil_health = relationship("SoilHealth", back_populates="user")
    bids = relationship("Bid", back_populates="user")
    schemes = relationship("Scheme", secondary="user_scheme", back_populates="users")
    produce_listings = relationship("ProduceListing", back_populates="user")