import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class CourseDepartmentMapping(Base):
    __tablename__ = "course_department_mapping"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    department_id = Column(Integer, ForeignKey("department.id"))
    is_active = Column(Boolean, default=False)
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"