import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class ConfigurationHistory(Base):
    __tablename__ = "configuration_history"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    version = Column(String)
    details = Column(JSON)
    status = Column(String)
    error = Column(String)
    created_by = Column(Integer, ForeignKey("institution_master.id"), index=True)
    updated_by = Column(Integer, ForeignKey("institution_master.id"))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"

    # possible status:
    # 1. inprogress
    # 2. completed
    # 3. failed
    # 4. cancelled 