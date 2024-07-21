import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class EntityMapping(Base):
    __tablename__ = "entity_mapping"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entity_master.id"))
    name = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"