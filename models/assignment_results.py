import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class AssignmentResults(Base):
    __tablename__ = "assignment_results"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignment.id"))
    user_id = Column(Integer, ForeignKey("user_master.id"))
    marks = Column(Float)
    status = Column(String)
    attempt_number = Column(Integer)
    submitted_data = Column(JSON)
    evaluation_data = Column(JSON)
    is_qualified = Column(Boolean, default=False)
    is_late = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # relations
    assignment = relationship("Assignment", backref=backref("assignment_results", passive_deletes=True))
    user = relationship("UserMaster", backref=backref("assignment_results", passive_deletes=True))

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"
