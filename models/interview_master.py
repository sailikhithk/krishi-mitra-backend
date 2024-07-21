import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class InterviewMaster(Base):
    __tablename__ = "interview_master"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    interview_type = Column(String(100)) # new column need to create this 
    specifications = Column(JSON)
    level = Column(String(100))
    status = Column(String(100))
    path_json = Column(JSON)               
    result_json = Column(JSON)
    report_json = Column(JSON)
    prioritize = Column(Boolean)
    improvement_areas_count = Column(Integer, default= 0)
    improvement_areas = Column(JSON, default= [])
    percentage = Column(Float)
    marks =  Column(Float)
    max_marks = Column(Float)
    skill_gap_rate = Column(Float)
    relevant_answers = Column(Integer)
    un_relevant_answers = Column(Integer)
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"