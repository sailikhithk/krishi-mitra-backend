import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class Assignment(Base):
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    skills_required = Column(String)
    max_time_min = Column(Integer)
    always_open_submission = Column(Boolean, default=True)
    deadline = Column(DateTime)
    auto_reminders = Column(Boolean, default=True)
    auto_assignment_notification = Column(Boolean, default=True)
    allows_late_submission = Column(Boolean, default=False)
    number_of_reattempt = Column(Integer)
    questions = Column(JSON)
    base_combination = Column(JSON)
    status = Column(String)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("user_master.id"))
    updated_by = Column(Integer, ForeignKey("user_master.id"))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # relations
    assignment_user_mapping = relationship(
        "AssignmentUserMapping",
        backref=backref("assignment", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"
