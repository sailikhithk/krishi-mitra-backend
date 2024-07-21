import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class PlacementDetails(Base):
    __tablename__ = "placement_details"
    id = Column(Integer, primary_key=True)
    institution_id = Column(Integer, ForeignKey("institution_master.id"), index=True)
    user_id = Column(Integer, ForeignKey("user_master.id"), index=True)
    company_name = Column(String(255))
    company_type = Column(String(255)) 
    offer = Column(String(255)) 
    offer_type = Column(String(255))
    status = Column(String(255), default="Not aplaced")
    
    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"