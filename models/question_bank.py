import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class QuestionBankMaster(Base):
    __tablename__ = "question_bank"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = Column(JSON)
    base_combination = Column(JSON)
    status = Column(String)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("user_master.id"))
    updated_by = Column(Integer, ForeignKey("user_master.id"))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"