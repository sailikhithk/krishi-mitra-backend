import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableDict

class TrainingCourseUserMapping(Base):
    __tablename__ = "training_course_user_mapping"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("training_course.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("user_master.id"))
    track = Column(MutableDict.as_mutable(JSON))
    status = Column(String, default='not_strated')
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"