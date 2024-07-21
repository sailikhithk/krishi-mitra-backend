import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref


class UserMaster(Base):
    __tablename__ = "user_master"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255), default="")
    phone_number = Column(String(255))
    address = Column(String(255))
    email = Column(String(255), unique=True)
    branch_id = Column(Integer, ForeignKey("branch.id"), index=True)
    department_id = Column(Integer, ForeignKey("department.id"), index=True)
    institution_id = Column(Integer, ForeignKey("institution_master.id"), index=True)
    programme = Column(String(255))
    certified_hard_skills = Column(String(1000)) 
    certified_soft_skills = Column(String(1000)) 
    uncertified_hard_skills = Column(String(1000))
    uncertified_soft_skills = Column(String(1000))
    negative_emotions = Column(String(1000))
    screening_id = Column(Integer)
    student_id = Column(String(255)) # new column need to create   
    # intermediate_hard_skills = Column(String(1000))
    # intermediate_soft_skills = Column(String(1000))

    hard_skill_avg_score = Column(String(1000))
    soft_skill_avg_score = Column(String(1000))
    
    course_id = Column(Integer, ForeignKey("course.id"))
    password_hash = Column(String(128))
    role_id = Column(Integer, ForeignKey("role.id"))
    number_of_interviews = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    initial_password_reset = Column(Boolean, default=False)
    password_modified_date = Column(DateTime)
    last_login_date = Column(DateTime)

    assignment_user_mapping = relationship(
        "AssignmentUserMapping",
        backref=backref("user_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    interview_master = relationship(
        "InterviewMaster",
        backref=backref("user_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    interview_master = relationship(
        "TrainingCourseUserMapping",
        backref=backref("user_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"