from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Float, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    ADMIN = "admin"
    LOGISTICS = "logistics"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    phone_number = Column(String, unique=True, index=True)
    
    # Common fields
    full_name = Column(String)
    address = Column(String)
    aadhar_card_url = Column(String)  # URL to stored Aadhar card image
    
    # Farmer specific fields
    farm_size = Column(Float)
    location = Column(String)
    soil_type = Column(String)
    irrigation_facilities = Column(String)
    crop_specialization = Column(JSON)  # Store as a list of strings
    certifications = Column(JSON)  # Store as a list of strings
    bank_account_details = Column(JSON)  # Store as a dictionary
    
    # Buyer specific fields
    company_name = Column(String)
    business_type = Column(String)
    
    # Logistics specific fields
    vehicle_type = Column(String)
    vehicle_number = Column(String)
    has_smartphone = Column(Boolean, default=False)
    
    # Admin specific fields
    department = Column(String)
    access_level = Column(String)

    soil_health = relationship("SoilHealth", back_populates="user")
    bids = relationship("Bid", back_populates="user")
    schemes = relationship("Scheme", secondary="user_scheme", back_populates="users")
    produce_listings = relationship("ProduceListing", back_populates="user")
    logistics_bookings = relationship("Logistics", back_populates="logistics_personnel")