import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class ScreeningMaster(Base):
    __tablename__ = "screening_master"
    id = Column(Integer, primary_key=True)
    unique_code = Column(String(255), unique=True)
    name = Column(String(255))
    max_capacity = Column(Integer)
    description = Column(String(255))
    activation_date = Column(DateTime)
    expiry_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey("institution_master.id"))
    updated_by = Column(Integer, ForeignKey("institution_master.id"))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"