import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship, backref

class InstitutionMaster(Base):
    __tablename__ = "institution_master"

    id = Column(Integer, primary_key=True)
    institution_name = Column(String(255), index=True, unique=True)
    contact_name = Column(String(255))
    email = Column(String(255), unique=True)
    phone_number = Column(String(255))
    country_id = Column(Integer, ForeignKey("country.id"))
    city = Column(String(255))
    desiganation = Column(String(255))
    number_of_students = Column(Integer, default=0)
    # students_cap = Column(Integer, default=0)
    # interview_per_month = Column(Integer, default=0)
    number_of_departments = Column(Integer, default=0)
    registration_number = Column(String(255))
    domains = Column(String(255), default="")
    preference_days = Column(String(255), default="mon")
    preference_time = Column(String(255))
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    interview_questions_mode = Column(String(255))
    initial_configuration = Column(Boolean, default=False)
    configuration_version = Column(JSON)
    latest_configuration_date = Column(DateTime)
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    password_modified_date = Column(DateTime)
    last_login_date = Column(DateTime)

    # relations
    institution_branch_mapping = relationship(
        "InstitutionBranchMapping",
        backref=backref("institution_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    institution_company_mapping = relationship(
        "InstitutionCompanyMapping",
        backref=backref("institution_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    institution_hard_skill_mapping = relationship(
        "InstitutionHardSkillMapping",
        backref=backref("institution_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )
    
    institution_soft_skill_mapping = relationship(
        "InstitutionSoftSkillMapping",
        backref=backref("institution_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    user_master = relationship(
        "UserMaster",
        backref=backref("institution_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    screening_master = relationship(
        "ScreeningMaster",
        primaryjoin="InstitutionMaster.id == ScreeningMaster.created_by",
        foreign_keys="[ScreeningMaster.created_by, ScreeningMaster.updated_by]",
        backref=backref("institution_master", passive_deletes=True),
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        attributes = ', '.join([f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_')])
        return f"<{self.__class__.__name__}({attributes})>"
