import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class TrainingCourse(Base):
    __tablename__ = "training_course"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String)
    unique_code = Column(String(100), unique=True)
    stage = Column(Integer)
    created_by = Column(Integer, ForeignKey("user_master.id"))
    updated_by = Column(Integer, ForeignKey("user_master.id"))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # relations
    course_user_mapping = relationship(
        "TrainingCourseUserMapping",
        backref=backref("training_course", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"


# Stage Numbers:
# 1 step-1 completed
# 2 step-2 completed
# 3 step-3 completed
