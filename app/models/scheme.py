from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base
from app.models.user import user_scheme

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    eligibility = Column(String)
    benefits = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", secondary=user_scheme, back_populates="schemes")
