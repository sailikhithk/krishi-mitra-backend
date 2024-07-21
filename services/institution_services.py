import traceback
import uuid
import random
import base64
import json
import os
from openpyxl import Workbook
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import asc, desc, cast, Integer, func, update


from models import (InstitutionMaster, Country, Role, UserMaster, Branch, 
                    Department, Course, HardSkill, SoftSkill, WorkingRole, Company, 
                    InterviewMaster, BranchCourseMapping, CourseDepartmentMapping,
                    InstitutionBranchMapping, CourseDepartmentMapping, BranchCourseMapping, 
                    InstitutionHardSkillMapping, InstitutionSoftSkillMapping, InstitutionCompanyMapping,
                    ConfigurationHistory, ScreeningMaster, PlacementDetails                    
                    )

from collection_models import (HardSkillCustomQuestions, SoftSkillCustomQuestions, CompanyRoleCustomQuestions)

from email_utils import send_email
from database import session
from ai_generator import (generate_skill_questions, generate_skill_improvement_suggestions, 
                          generate_company_questions, generate_company_related_data,
                          generate_working_role_related_data
                        )
from google_module.google_drive import GoogleDriveManager

from utils import encrypt, decrypt, obj_to_dict, obj_to_list, query_to_dataframe, identify_list_differences
from meta_data import BACKEND_SERVER_URL, UI_SERVER_URL, UPLOAD_USER_FILE_PLACEMENT_TRACKER_HEADERS
from flask_jwt_extended import create_access_token
class InstitutionService:
    def __init__(self):
        pass
    
    # Hard Skills CRUD
    def create_hard_skills(self, name):
        name = name.title()
        skill_id = None
        existing = session.query(HardSkill).filter_by(name=name).first()
        if not existing:
            role = HardSkill(name=name)
            session.add(role)
            session.commit()
            skill_id = role.id
        else:
            skill_id = existing.id
        print(f"Hard skill {name} created")
        return skill_id

    def create_hard_skills_mapping(self, institution_id, institution_name, skill_id, name):
        existing = session.query(InstitutionHardSkillMapping).filter_by(institution_id=institution_id).filter_by(skill_id=skill_id).first()
        if not existing:
            role = InstitutionHardSkillMapping(
                institution_id=institution_id,
                skill_id=skill_id,
                is_active=True
                )
            session.add(role)
        session.commit()
        print(f"Hard skill {name} mapped with institution {institution_name}")

    def delete_hard_skills(self, name):
        existing = session.query(HardSkill).filter_by(name=name).first()
        if existing:
            session.delete(existing)
        session.commit()
        print(f"Hard skill {name} deleted")

    def delete_hard_skills_mapping(self, institution_id, institution_name, skill_id, name):
        existing_mappings = session.query(InstitutionHardSkillMapping).filter_by(institution_id=institution_id).filter_by(skill_id=skill_id).all()
        for mapping in existing_mappings:
            session.delete(mapping)
        session.commit()
        print(f"Hard skill {name} mapping deleted with institution {institution_name}")

    def hard_skills_list(self, user_id=None, institution_id=None):
        if user_id:
            user_obj = session.query(UserMaster).filter_by(id = user_id).first()
            institution_id = user_obj.institution_id
        
        if institution_id:
            records = session.query(
                HardSkill.id.label('id'),
                HardSkill.name.label('name'),
                )\
                .join(InstitutionHardSkillMapping, HardSkill.id == InstitutionHardSkillMapping.skill_id)\
                .filter(InstitutionHardSkillMapping.institution_id == institution_id)\
                .filter(InstitutionHardSkillMapping.is_active == True)\
                .order_by(HardSkill.name)\
                .distinct()    
            data_list = [
                    {
                        "id": record.id,
                        "name": record.name
                    } for record in records
                ]
        else:
            data_list = []
        return data_list
        
        # data = session.query(SoftSkill).order_by(SoftSkill.name).all()    
        # return obj_to_list(data)
    
    # Soft Skills CRUD
    def create_soft_skills(self, name):
        name = name.title()
        skill_id = None
        existing = session.query(SoftSkill).filter_by(name=name).first()
        if not existing:
            role = SoftSkill(name=name)
            session.add(role)
            session.commit()
            skill_id = role.id
        else:
            skill_id = existing.id
        print(f"Soft skill {name} created")
        return skill_id

    def create_soft_skills_mapping(self, institution_id, institution_name, skill_id, name):
        existing = session.query(InstitutionSoftSkillMapping).filter_by(institution_id=institution_id).filter_by(skill_id=skill_id).first()
        if not existing:
            role = InstitutionSoftSkillMapping(
                institution_id=institution_id,
                skill_id=skill_id,
                is_active=True
                )
            session.add(role)
        session.commit()
        print(f"Soft skill {name} mapped with institution {institution_name}")

    def delete_soft_skills(self, name):
        existing = session.query(SoftSkill).filter_by(name=name).first()
        if existing:
            session.delete(existing)
        session.commit()
        print(f"Soft skill {name} deleted")
    
    def delete_soft_skills_mapping(self, institution_id, institution_name, skill_id, name):
        existing_mappings = session.query(InstitutionSoftSkillMapping).filter_by(institution_id=institution_id).filter_by(skill_id=skill_id).all()
        for mapping in existing_mappings:
            session.delete(mapping)
        session.commit()
        print(f"Soft skill {name} mapping deleted with institution {institution_name}")

    def soft_skills_list(self, user_id=None, institution_id=None):
        if user_id:
            user_obj = session.query(UserMaster).filter_by(id = user_id).first()
            institution_id = user_obj.institution_id
        
        if institution_id:
            records = session.query(
                SoftSkill.id.label('id'),
                SoftSkill.name.label('name'),
                )\
                .join(InstitutionSoftSkillMapping, SoftSkill.id == InstitutionSoftSkillMapping.skill_id)\
                .filter(InstitutionSoftSkillMapping.institution_id == institution_id)\
                .filter(InstitutionSoftSkillMapping.is_active == True)\
                .order_by(SoftSkill.name)\
                .distinct()    
            data_list = [
                    {
                        "id": record.id,
                        "name": record.name
                    } for record in records
                ]
        else:
            data_list = []
        return data_list
        
        # data = session.query(HardSkill).order_by(HardSkill.name).all()    
        # return obj_to_list(data)
    
    # Working Roles CRUD
    def create_working_roles(self, name):
        name = name.title()
        role_id = None
        existing = session.query(WorkingRole).filter_by(name=name).first()
        if not existing:
            responsibilities, top_skills = generate_working_role_related_data(name)
            role = WorkingRole(
                name=name,
                responsibilities=responsibilities,
                skills=top_skills
                )
            session.add(role)
            session.commit()
            role_id = role.id
        else:
            role_id = existing.id
        print(f"Working Role {name} created")
        return role_id
    
    # Company CRUD
    def create_new_company(self, name):
        name = name.title()
        company_id = None
        existing = session.query(Company).filter_by(name=name).first()
        print(f"Creating Company {name}")
        if not existing:
            about_company, latest_news, industry_trends = generate_company_related_data(name)
            role = Company(
                name=name,
                about_company = about_company,
                latest_news = latest_news,
                industry_trends = industry_trends
            )
            session.add(role)
            session.commit()
            company_id = role.id
        else:
            company_id = existing.id
        print(f"Company {name} created")
        return company_id
    
    def create_company_mapping(self, institution_id, company_id, role_ids, name):
        existing = session.query(InstitutionCompanyMapping).filter_by(institution_id=institution_id).filter_by(company_id=company_id).first()
        if not existing:
            role = InstitutionCompanyMapping(
                institution_id=institution_id,
                company_id=company_id,
                is_active=True,
                role_ids = role_ids
                )
            session.add(role)
        else:
            existing.role_ids = role_ids

        session.commit()
        print(f"Company {name} is mapped with institution {institution_id}")

    def delete_company_mapping(self, institution_id, company_id, name):
        existing_mappings = session.query(InstitutionCompanyMapping).filter_by(institution_id=institution_id).filter_by(company_id=company_id).all()
        for mapping in existing_mappings:
            session.delete(mapping)
        session.commit()
        print(f"Company {name} mapping deleted with institution {institution_id}")
    
    def companies_list(self, user_id=None, institution_id=None):
        if user_id:
            user_obj = session.query(UserMaster).filter_by(id = user_id).first()
            institution_id = user_obj.institution_id
        
        if institution_id:
            records = session.query(
                Company.id.label('id'),
                Company.name.label('name'),
                InstitutionCompanyMapping.role_ids.label('role_ids'),
                )\
                .join(InstitutionCompanyMapping, Company.id == InstitutionCompanyMapping.company_id)\
                .filter(InstitutionCompanyMapping.institution_id == institution_id)\
                .filter(InstitutionCompanyMapping.is_active == True)\
                .order_by(Company.name)\
                .distinct()    
            data_list = [
                    {
                        "id": record.id,
                        "name": record.name,
                        "role_ids": record.role_ids 
                    } for record in records
                ]
        else:
            data_list = []
        return data_list

        # data = session.query(Company).order_by(Company.name).all()
        # return obj_to_list(data)

    
    # Institution CRUD
    def get_institution_by_id(self, id):
        return session.query(InstitutionMaster).filter_by(id = id).first()        
        
    def get_institution_by_email(self, email):
        return session.query(InstitutionMaster).filter_by(email = email).first()        
            
    # def interview_roles_list(self):  # Harnath Need to fix this
    #     data = session.query(WorkingRole).order_by(WorkingRole.name).all()    
    #     return obj_to_list(data)
    
    def get_interview_roles_list_names(self, roles_id_list, format='list'):
        roles = session.query(WorkingRole).filter(WorkingRole.id.in_(roles_id_list)).all()    
        roles_sorted = sorted(roles, key=lambda role: role.name)
        if format == 'list':
            names = [role.name for role in roles_sorted]
        elif format == 'list(dict)':
            names = [{"name": role.name, "id":role.id} for role in roles_sorted]
        return names
    
    def get_interview_roles_list_ids(self, roles_name_list):
        roles = session.query(WorkingRole).filter(WorkingRole.name.in_(roles_name_list)).all()
        
        existing_role_names = {role.name for role in roles}

        ids = [role.id for role in roles]

        for role_name in roles_name_list:
            if role_name not in existing_role_names:
                new_role_id = self.create_working_roles(role_name)
                if new_role_id:
                    ids.append(new_role_id)    
                
        return ids
    
    def get_institution_config(self, user_id=None, institution_id=None):
        if user_id:
            user_obj = session.query(UserMaster).filter_by(id = user_id).first()
            institution_id = user_obj.institution_id
        
        if institution_id:
            records = session.query(
                InstitutionMaster.id.label('institution_id'),
                InstitutionMaster.institution_name.label('institution_name'),
                InstitutionBranchMapping.branch_id.label('branch_id'),
                Branch.name.label('branch_name'),
                BranchCourseMapping.course_id.label('course_id'),
                Course.name.label('course_name'),
                CourseDepartmentMapping.department_id.label('department_id'),
                Department.name.label('department_name')
                )\
                .join(InstitutionBranchMapping, InstitutionMaster.id == InstitutionBranchMapping.institution_id)\
                .join(Branch, Branch.id == InstitutionBranchMapping.branch_id)\
                .join(BranchCourseMapping, BranchCourseMapping.branch_id == Branch.id)\
                .join(Course, Course.id == BranchCourseMapping.course_id)\
                .join(CourseDepartmentMapping, CourseDepartmentMapping.course_id == Course.id)\
                .join(Department, Department.id == CourseDepartmentMapping.department_id)\
                .filter(InstitutionMaster.id == institution_id)\
                .order_by(InstitutionMaster.institution_name)\
                .order_by(Branch.name)\
                .order_by(Course.name)\
                .distinct()
            
            data_list = [
                    {
                        "institution_id": record.institution_id,
                        "institution_name": record.institution_name,
                        "branch_id": record.branch_id,
                        "branch_name": record.branch_name,
                        "course_id": record.course_id,
                        "course_name": record.course_name,
                        "department_id": record.department_id,
                        "department_name": record.department_name
                    } for record in records
                ]
        else:
            data_list = []
        return data_list
    
    def institution_list(self):
        institution = session.query(InstitutionMaster.id, InstitutionMaster.institution_name).order_by(InstitutionMaster.institution_name).all()    
        list_dicts = [{"id": row.id, "institution_name": row.institution_name} for row in institution]

        return list_dicts
    
    def delete_institution(self, institution_id):
        try:
            institution = session.query(InstitutionMaster).get(institution_id)
            
            if institution:
                session.delete(institution)
                session.commit()
                return {"status": True, "message": "Institution Deleted"} 
            else:
                return {"status": False, "message": "Institution not deleted"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
        
    def activate_institution(self, institution_id):
        try:
            institution = session.query(InstitutionMaster).get(institution_id)
            
            if institution:
                institution.is_active = True
                session.commit()
                return {"status": True, "message": "Institution Activated"} 
            else:
                return {"status": False, "message": "Institution not Activated"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def deactive_institution(self, institution_id):
        try:
            institution = session.query(InstitutionMaster).get(institution_id)
            
            if institution:
                institution.is_active = False
                session.commit()
                return {"status": True, "message": "Institution Deactivated"} 
            else:
                return {"status": False, "message": "Institution not Deactivated"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}

    # Country CRUD
    def country_list(self):
        data = session.query(Country).order_by(Country.name).all()
        return obj_to_list(data)
    
    # Branch CRUD
    def create_branch(self, name):
        name = name.title()
        branch_id = None
        existing = session.query(Branch).filter_by(name=name).first()
        print(f"Creating branch {name}")
        if not existing:
            role = Branch(
                name=name
            )
            session.add(role)
            session.commit()
            branch_id = role.id
        else:
            branch_id = existing.id
        print(f"branch {name} created")
        return branch_id

    def delete_institution_branch_mapping(self, institution_id, branch_id, institution_name, branch_name):
        existing_mappings = session.query(InstitutionBranchMapping).filter_by(institution_id=institution_id).filter_by(branch_id=branch_id).all()
        for mapping in existing_mappings:
            session.delete(mapping)
        session.commit()
        print(f"Branch {branch_name} mapping deleted with institution {institution_name}")

    def create_institution_branch_mapping(self, institution_id, branch_id, institution_name, branch_name):
        existing = session.query(InstitutionBranchMapping).filter_by(institution_id=institution_id).filter_by(branch_id=branch_id).first()
        if not existing:
            role = InstitutionBranchMapping(
                institution_id=institution_id,
                branch_id=branch_id,
                is_active=True,
                )
            session.add(role)
        
        session.commit()
        print(f"Branch {branch_name} is mapped with institution {institution_name}")
    
    def branch_list(self, institution_id):
        if institution_id:
            records = session.query(
                Branch.id.label('id'),
                Branch.name.label('name'),
                )\
                .join(InstitutionBranchMapping, Branch.id == InstitutionBranchMapping.branch_id)\
                .filter(InstitutionBranchMapping.institution_id == institution_id)\
                .order_by(Branch.name)\
                .distinct()    
            
            data_list = [
                {
                    "id": record.id,
                    "name": record.name
                } for record in records
            ]
            return data_list
        else:
            return []
        
    # Department CRUD
    def department_list(self, course_id):
        if course_id:
            records = session.query(
                Department.id.label('id'),
                Department.name.label('name'),
                )\
                .join(CourseDepartmentMapping, Department.id == CourseDepartmentMapping.department_id)\
                .filter(CourseDepartmentMapping.course_id == course_id)\
                .order_by(Department.name)\
                .distinct()
            
            data_list = [
                {
                    "id": record.id,
                    "name": record.name
                } for record in records
            ]
            return data_list  
        else:
            return []
        
    def create_department(self, department):
        department = department.title()
        department_id = None
        existing = session.query(Department).filter_by(name=department).first()
        print(f"Creating department {department}")
        if not existing:
            role = Department(
                name=department
            )
            session.add(role)
            session.commit()
            department_id = role.id
        else:
            department_id = existing.id
        print(f"department {department} created")
        return department_id
    
    def create_course_department_mapping(self, course_id, department_id, course_name, department_name):
        existing = session.query(CourseDepartmentMapping).filter_by(course_id=course_id).filter_by(department_id=department_id).first()
        if not existing:
            role = CourseDepartmentMapping(
                course_id=course_id,
                department_id=department_id,
                is_active=True,
                )
            session.add(role)
        
        session.commit()
        print(f"department {department_name} is mapped with course {course_name}")
    
    def delete_course_department_mapping(self, course_id, department_id, course_name, department_name):
        existing_mappings = session.query(CourseDepartmentMapping).filter_by(course_id=course_id).filter_by(department_id=department_id).all()
        for mapping in existing_mappings:
            session.delete(mapping)
        session.commit()
        print(f"department {department_name} mapping deleted with course {course_name}")
        
    # Course CRUD
    def course_list(self, branch_id):
        if branch_id:
            records = session.query(
                Course.id.label('id'),
                Course.name.label('name'),
                )\
                .join(BranchCourseMapping, Course.id == BranchCourseMapping.course_id)\
                .filter(BranchCourseMapping.branch_id == branch_id)\
                .order_by(Course.name)\
                .distinct()
            
            data_list = [
                {
                    "id": record.id,
                    "name": record.name
                } for record in records
            ]
            return data_list  
        else:
            return []

    def create_course(self, name):
        name = name.title()
        course_id = None
        existing = session.query(Course).filter_by(name=name).first()
        print(f"Creating course {name}")
        if not existing:
            role = Course(name=name)
            session.add(role)
            session.commit()
            course_id = role.id
        else:
            course_id = existing.id
        print(f"course {name} created")
        return course_id
    
    def create_branch_course_mapping(self, branch_id, course_id, branch_name, course_name):
        existing = session.query(BranchCourseMapping).filter_by(branch_id=branch_id).filter_by(course_id=course_id).first()
        if not existing:
            role = BranchCourseMapping(
                course_id=course_id,
                branch_id=branch_id,
                is_active=True,
                )
            session.add(role)
        
        session.commit()
        print(f"Course {course_name} is mapped with branch {branch_name}")
    
    def delete_branch_course_mapping(self, branch_id, course_id, branch_name, course_name):
        existing_mappings = session.query(BranchCourseMapping).filter_by(course_id=course_id).filter_by(branch_id=branch_id).all()
        for mapping in existing_mappings:
            session.delete(mapping)
        session.commit()
        print(f"course {course_name} mapping deleted with branch {branch_name}")

    def login_institution(self, data):
        try:
            email = data["email"]
            email = str(email).strip().lower()
            password = data["password"]
            
            institution = self.get_institution_by_email(email)
            if not institution:
                return {"message": "Invalid username or password", "status": False}

            if not institution.is_active:
                return {"message": "User deactivated contact admin", "status": False}
            
            
            hashpwd = institution.password_hash
            db_password = decrypt(hashpwd)

            if db_password == password:
                institution_data = obj_to_dict(institution)
                role_name = "Admin"
                role = session.query(Role).filter_by(name = role_name).first()
                role_id = role.id
                institution_data["role_id"] = role_id
                institution_data["role_name"] = role_name
                access_token = create_access_token(identity=institution_data)
                return {"message": "", "status": True, "access_token": access_token, "data": institution_data}
            else:
                return {"message": "Invalid username or password", "status": False}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def reset_password(self, data):
        try:
            password = data["new_password"]
            email = data["email"]
            hashed_password = encrypt(password)
            email = str(email).strip().lower()
            
            institution = self.get_institution_by_email(email)
            if not institution:
                return {"message": "Invalid creds", "status": False}        
            institution.password_hash = hashed_password
            institution.password_modified_date = datetime.now()
            session.commit()
            return {"message": "Password updated, relogin again", "status": True}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def update_password(self, data, institution_id):
        try:
            password = data["new_password"]
            hashed_password = encrypt(password)
            
            institution = self.get_institution_by_id(institution_id)
            if not institution:
                return {"message": "Invalid creds", "status": False}        
            institution.password_hash = hashed_password
            institution.password_modified_date = datetime.now()
            session.commit()
            return {"message": "Password updated, relogin again", "status": True}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}

    def register_institution(self, data):
        try:
            data["password_hash"] = encrypt(data["password"])
            original_password = data["password"]
            data.pop("password")
            email = str(data["email"]).strip().lower()
            
            existing_institution = self.get_institution_by_email(email)
            if existing_institution:
                return {"status": False, "message": "Institution with same email exists"}
            
            institution = InstitutionMaster(**data)
            session.add(institution)
            session.commit()
            institution_dic = obj_to_dict(institution)
            institution_dic.pop("password_hash", None)
            if institution_dic:
                email_values = {
                    "user_name": institution.email,
                    "institution_name": institution.institution_name,
                    "password": original_password,
                    "login_url": UI_SERVER_URL    
                }
                send_email("institution_register.html",institution.email, "Institution Registered", email_values)
                return {"status": True, "message": "Institution Created", "data":institution_dic} 
            else:
                return {"status": False, "message": "Institution not created"} 
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def update_institution(self, institution_id, update_data):
        try:
            institution = session.query(InstitutionMaster).get(institution_id)
            
            if institution:
                for key, value in update_data.items():
                    setattr(institution, key, value)  
                session.commit()
            institution_dic = obj_to_dict(institution)
            institution_dic.pop("password_hash", None)
            if institution_dic:
                return {"status": True, "message": "Institution Updated", "data":institution_dic}
            else:
                return {"status": False, "message": "Institution not updated"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def list_institutions_with_filters(self, institution_id, page=1, per_page=20, sort_by=None, sort_order='asc'):
        try:
            sort_order = sort_order.lower()
            if sort_order not in ['asc', 'desc']:
                sort_order = 'desc'

            if sort_by not in ['institution_name', 'contact_name', 'email', 'created_date']:
                sort_by = 'institution_name'

            institutions_query = session.query(InstitutionMaster).filter_by(id = institution_id)

            if sort_order == 'asc':
                institutions_query = institutions_query.order_by(asc(sort_by))
            else:
                institutions_query = institutions_query.order_by(desc(sort_by))

            total_count = institutions_query.count()

            total_pages = (total_count + per_page - 1) // per_page

            page = min(max(1, page), total_pages)

            next_page_number = None if page >= total_pages else page + 1
            prev_page_number = None if page <= 1 else page - 1

            institutions = institutions_query.limit(per_page).offset((page - 1) * per_page).all()

            institutions_list = obj_to_list(institutions)

            meta_data = {
                "total": total_count,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "next_page_number": next_page_number,
                "prev_page_number": prev_page_number
            }

            response = {
                "data": institutions_list,
                "meta_data": meta_data,
                "status": True
            }

            return response
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

        
    def management(self, institution_id):
        try:
            students_obj = session.query(UserMaster).join(Role).filter(UserMaster.institution_id == institution_id).filter(Role.name == 'Student').all()
            teachers_obj = session.query(UserMaster).join(Role).filter(UserMaster.institution_id == institution_id).filter(Role.name == 'Teacher').all()

            students = obj_to_list(students_obj)
            teachers = obj_to_list(teachers_obj)
            students_df = pd.DataFrame(students)
            teachers_df = pd.DataFrame(teachers)
            print("students_df", students_df)
            print("teachers_df", teachers_df)
            if len(students_df):
                unique_student_departments = students_df["department_id"].nunique()
                unique_student_branchs = students_df["branch_id"].nunique()
            else:
                unique_student_departments = 0
                unique_student_branchs = 0
            
            
            if len(teachers_df):
                unique_teacher_departments = teachers_df["department_id"].nunique()            
                unique_teacher_branchs = teachers_df["branch_id"].nunique()
            else:
                unique_teacher_departments = 0
                unique_teacher_branchs = 0
                        
            response = {
                "students": {
                    "number_of_students": len(students),
                    "number_of_departments": unique_student_departments,
                    "number_of_branches": unique_student_branchs

                },
                "teachers": {
                    "number_of_teachers": len(teachers),
                    "number_of_departments": unique_teacher_departments,
                    "number_of_branches": unique_teacher_branchs
                }
            }
            return response
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def get_week_start_and_end_dates(self, week_no, year):
        """
        Get the start and end dates of a week given its week number and year.
        """
        jan_1 = datetime(year, 1, 1)
        days_to_add = timedelta(days=(week_no - 1) * 7)
        week_start_date = jan_1 + days_to_add - timedelta(days=jan_1.weekday())
        week_end_date = week_start_date + timedelta(days=6)
        return week_start_date, week_end_date
    
    def get_week_number_based_on_date(self, date):
        if date is None:
            date = datetime.now()
        current_year, current_week_no, _ = date.isocalendar()
        return current_week_no
    
    def default_branch_by_institution_id(self, institution_id):
        branch_list_result = self.branch_list(institution_id)
        if branch_list_result:
            branch_id =  branch_list_result[0]["id"]
            branch_name = branch_list_result[0]["name"]
        else:
            branch_id = None
            branch_name = None
        return branch_id, branch_name
        
    def default_course_by_branch_id(self, branch_id):
        course_list_result = self.course_list(branch_id)
        if course_list_result:
            course_id =  course_list_result[0]["id"]
            course_name = course_list_result[0]["name"]
        else:
            course_id = None
            course_name = None
        return course_id, course_name
    
    def default_department_by_course_id(self, course_id):
        department_list_result = self.department_list(course_id)
        if department_list_result:
            department_id =  department_list_result[0]["id"]
            department_name = department_list_result[0]["name"]
        else:
            department_id = None
            department_name = None
        return department_id, department_name
    
    def institution_statistics(self, institution_id, filters = {}):
        try:
            department_obj = None
            institution_obj = session.query(InstitutionMaster).filter_by(id = institution_id).first()
            if not institution_obj:
                return {"status": False, "message": "Wrong institution"}    
            
            # Primary Querys
            role_obj = session.query(Role).filter_by(name = "Student").first()
            student_role_id = role_obj.id
            role_obj = session.query(Role).filter_by(name = "Teacher").first()
            teacher_role_id = role_obj.id

            active_students = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(is_active = True).filter_by(role_id = student_role_id)
            
            inactive_students = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(is_active = False).filter_by(role_id = student_role_id)
            
            active_teachers = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(is_active = True).filter_by(role_id = teacher_role_id)
            
            inactive_teachers = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(is_active = False).filter_by(role_id = teacher_role_id)
            
            interviews = session.query(InterviewMaster, InstitutionMaster, UserMaster)\
                        .join(UserMaster, InterviewMaster.user_id == UserMaster.id)\
                        .join(InstitutionMaster, UserMaster.institution_id == InstitutionMaster.id)

            improvement_areas_identified_query = session.query(func.avg(InterviewMaster.improvement_areas_count))\
                .select_from(InterviewMaster)\
                .join(UserMaster, InterviewMaster.user_id == UserMaster.id)\
                .join(InstitutionMaster, UserMaster.institution_id == InstitutionMaster.id)\
            
            average_interview_score_query = session.query(func.avg(InterviewMaster.percentage))\
                .select_from(InterviewMaster)\
                .join(UserMaster, InterviewMaster.user_id == UserMaster.id)\
                .join(InstitutionMaster, UserMaster.institution_id == InstitutionMaster.id)
            
            skill_gap_rate_query = session.query(func.avg(InterviewMaster.skill_gap_rate))\
                .select_from(InterviewMaster)\
                .join(UserMaster, InterviewMaster.user_id == UserMaster.id)\
                .join(InstitutionMaster, UserMaster.institution_id == InstitutionMaster.id)
            
            # Branch Filter Block 
            layer_level  = "Branch" # as of now no use
            branch_id = None    
            branch_name = None
            if "branch" in filters:
                layer_level = "Course" # as of now no use
                branch_name = filters["branch"].replace("+", " ")
                branch_obj = session.query(Branch).filter_by(name = branch_name).first()
                if branch_obj:
                    branch_id = branch_obj.id
                else:
                    branch_id, branch_name = self.default_branch_by_institution_id(institution_id)            
            else:
                branch_id, branch_name = self.default_branch_by_institution_id(institution_id)            

            active_students = active_students.filter_by(branch_id = branch_id)
            inactive_students = inactive_students.filter_by(branch_id = branch_id)
            active_teachers = active_teachers.filter_by(branch_id = branch_id)
            inactive_teachers = inactive_teachers.filter_by(branch_id = branch_id)
            
            interviews = interviews.filter(UserMaster.branch_id == branch_id)

            improvement_areas_identified_query = improvement_areas_identified_query.filter(UserMaster.branch_id == branch_id)
            average_interview_score_query = average_interview_score_query.filter(UserMaster.branch_id == branch_id)
            skill_gap_rate_query = skill_gap_rate_query.filter(UserMaster.branch_id == branch_id)
            
            filters["branch_id"] = branch_id
            filters["branch"] = branch_name

            # Course Filter Block
            course_id = None    
            course_name = None
            if "course" in filters:
                layer_level  = "Department" # as of now no use
                course_name = filters["course"].replace("+", " ")
                course_obj = session.query(Course).filter_by(name = course_name).first()
                course_id = None
                if course_obj:
                    course_id = course_obj.id
                else:
                    course_id, course_name = self.default_course_by_branch_id(branch_id)            
            else:
                course_id, course_name = self.default_course_by_branch_id(branch_id)
            
            active_students = active_students.filter_by(course_id = course_id)
            inactive_students = inactive_students.filter_by(course_id = course_id)
            active_teachers = active_teachers.filter_by(course_id = course_id)
            inactive_teachers = inactive_teachers.filter_by(course_id = course_id)
            
            interviews = interviews.filter(UserMaster.course_id == course_id)

            improvement_areas_identified_query = improvement_areas_identified_query.filter(UserMaster.course_id == course_id)
            average_interview_score_query = average_interview_score_query.filter(UserMaster.course_id == course_id)
            skill_gap_rate_query = skill_gap_rate_query.filter(UserMaster.course_id == course_id)

            filters["course_id"] = course_id
            filters["course"] = course_name

            # Department Filter Block
            # department_id = None    
            # department_name = None
            # if "department" in filters:
            #     layer_level  = "User" # as of now no use
            #     department_name = filters["department"].replace("+", " ")
            #     department_obj = session.query(Department).filter_by(name = department_name).first()
            #     if department_obj:
            #         department_id = department_obj.id
            #     else:
            #         department_id, department_name = self.default_department_by_course_id(course_id)
            # else:
            #     department_id, department_name = self.default_department_by_course_id(course_id)
            
            # active_students = active_students.filter_by(department_id = department_id)
            # inactive_students = inactive_students.filter_by(department_id = department_id)
            # active_teachers = active_teachers.filter_by(department_id = department_id)
            # inactive_teachers = inactive_teachers.filter_by(department_id = department_id)
            
            # interviews = interviews.filter(UserMaster.department_id == department_id)

            # improvement_areas_identified_query = improvement_areas_identified_query.filter(UserMaster.department_id == department_id)
            # average_interview_score_query = average_interview_score_query.filter(UserMaster.department_id == department_id)
            # skill_gap_rate_query = skill_gap_rate_query.filter(UserMaster.department_id == department_id)
            
            # filters["department_id"] = department_id
            # filters["department"] = department_name

            # if "start_date" in filters:
            #     start_date = filters["start_date"]
            #     end_date = filters["end_date"]
            #     start_date = datetime.strptime(start_date, '%Y-%m-%d')
            #     end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # else:
            #     current_date = datetime.now()
            #     end_date = current_date + timedelta(days=1)
            #     start_date = current_date - timedelta(days=7)                
            #     filters["start_date"] = start_date.strftime("%Y-%m-%d")
            #     filters["end_date"] = end_date.strftime("%Y-%m-%d")

            # interviews = interviews.filter(InterviewMaster.created_date >= start_date, InterviewMaster.created_date < end_date)
            # improvement_areas_identified_query = improvement_areas_identified_query.filter(InterviewMaster.created_date >= start_date, InterviewMaster.created_date < end_date)
            # average_interview_score_query = average_interview_score_query.filter(InterviewMaster.created_date >= start_date, InterviewMaster.created_date < end_date)

            active_students_count = active_students.count()
            inactive_students_count = inactive_students.count()
            
            active_teachers_count = active_teachers.count()
            inactive_teachers_count = inactive_teachers.count()

            interviews = interviews.filter(InterviewMaster.status == 'report_generated')
            interviews_count = interviews.count()
        
            jd_interviews_obj = interviews.filter(InterviewMaster.status == 'report_generated').filter(InterviewMaster.interview_type == 'jd_interview').all()
            jd_interviews_count = len(jd_interviews_obj)
            
            cultural_interviews_obj = interviews.filter(InterviewMaster.status == 'report_generated').filter(InterviewMaster.interview_type == 'cultural_interview').all()
            cultural_interviews_count = len(cultural_interviews_obj)
            
            print("active_students_count", active_students_count)
            print("inactive_students_count", inactive_students_count)
            print("active_teachers_count", active_teachers_count)
            print("inactive_teachers_count", inactive_teachers_count)
            print("interviews_count", interviews_count)

            card_1 = {
                "name": "Number of Students",
                "value": active_students_count + inactive_students_count,
                "sub_values": {
                    "active": active_students_count,
                    "in_active": inactive_students_count
                }                
            }

            card_2 = {
                "name": "Number of Teachers",
                "value": active_teachers_count + inactive_teachers_count,
                "sub_values": {
                    "active": active_teachers_count,
                    "in_active": inactive_teachers_count
                }                
            }
            
            card_3 = {
                "name": "Number of Interviews Conducted",
                "value": interviews_count
            }
            
            average_improvement_areas = improvement_areas_identified_query.scalar()
            if not average_improvement_areas:
                average_improvement_areas = 0
            average_improvement_areas = round((float(average_improvement_areas)))
            card_4 = {
                "name": "improvement areas identified",
                "value": average_improvement_areas
            }

            average_interview_score = average_interview_score_query.scalar()
            if not average_interview_score:
                average_interview_score = 0
            average_interview_score = "{:.2f}".format(float(average_interview_score))
            card_5 = {
                "name": "Average Interview Score",
                "value": f"{average_interview_score}%"
            }
            
            skill_gap_rate = skill_gap_rate_query.scalar()
            if not skill_gap_rate:
                skill_gap_rate = 0
            skill_gap_rate = "{:.2f}".format(float(skill_gap_rate))
            card_6 = {
                "name": "Skill Gap rate",
                "value": f"{skill_gap_rate}%"
            }

            response = {
                "cards": [],
                "graphs": []
            }
            
            card_7 = {
                "name": "Number of JD Interviews Conducted",
                "value": jd_interviews_count
            }
            
            card_8 = {
                "name": "Number of cultural Interviews Conducted",
                "value": cultural_interviews_count
            }
            
            response["cards"] = [card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8] 

            # unique depertment list 
            # based on depertment -> user list 
            # get unique user ids with at least one inter view 
            if 'department' in filters:
                unique_departments_obj = session.query(Department).filter_by(id = department_id).first()
                unique_departments = {unique_departments_obj.id: unique_departments_obj.name}
            
            elif 'course' in filters:
                unique_departments_obj = session.query(Department.id, Department.name)\
                .join(CourseDepartmentMapping, Department.id == CourseDepartmentMapping.department_id)\
                .filter(CourseDepartmentMapping.course_id == course_id)\
                .distinct()
                unique_departments = {row[0]:row[1] for row in unique_departments_obj.all()}
            
            elif 'branchs'in filters:
                course_ids_obj = session.query(BranchCourseMapping.course_id)\
                .filter(BranchCourseMapping.branch_id == branch_id)\
                .all()
                course_ids = [row[0] for row in course_ids_obj]
                
                unique_departments_obj = session.query(Department.id, Department.name)\
                .join(CourseDepartmentMapping, Department.id == CourseDepartmentMapping.department_id)\
                .filter(CourseDepartmentMapping.course_id.in_(course_ids))\
                .distinct()
                unique_departments = {row[0]:row[1] for row in unique_departments_obj.all()}
            
            else:
                branch_ids_obj = session.query(InstitutionBranchMapping.branch_id)\
                    .filter(InstitutionBranchMapping.institution_id == institution_id)\
                    .all()
                branch_ids = [row[0] for row in branch_ids_obj]

                course_ids_obj = session.query(BranchCourseMapping.course_id)\
                    .filter(BranchCourseMapping.branch_id.in_(branch_ids))\
                    .all()
                course_ids = [row[0] for row in course_ids_obj] 
                                
                unique_departments_obj = session.query(Department.id, Department.name)\
                    .join(CourseDepartmentMapping, Department.id == CourseDepartmentMapping.department_id)\
                    .filter(CourseDepartmentMapping.course_id.in_(course_ids))\
                    .distinct()  

                unique_departments = {row[0]:row[1] for row in unique_departments_obj.all()}
            
            graph_1_data = []
            graph_3_data = []

            for department_id, department_name in unique_departments.items():
                print(f"Looping for department: {department_name} with id: {department_id}")
                user_obj = session.query(UserMaster.id).filter_by(department_id = department_id).filter_by(role_id = student_role_id).all()
                user_ids = [row[0] for row in user_obj]
                filter_interviews = session.query(InterviewMaster.id, InterviewMaster.user_id, InterviewMaster.improvement_areas).filter(InterviewMaster.user_id.in_(user_ids)).all()  
                
                filter_interviews_df = pd.DataFrame(filter_interviews, columns=["interview_id", "user_id", "improvement_areas"])
                print("filter_interviews_df", filter_interviews_df)

                filter_interviews_df['improvement_areas'] = filter_interviews_df['improvement_areas'].apply(lambda x: x if isinstance(x, list) else [])
                participated_user_ids = filter_interviews_df['user_id'].nunique()

                unique_improvement_areas = list(set([item for sublist in filter_interviews_df['improvement_areas'] for item in sublist]))
                if unique_improvement_areas:
                   max_count_unique_improvement_areas = max(unique_improvement_areas)
                else:
                    max_count_unique_improvement_areas = 0 
                graph_1_data.append({
                    "name": department_name,
                    "Participated": participated_user_ids,
                    "Not yet Participated": len(user_ids) - participated_user_ids
                })

                graph_3_data.append(
                    {"name": department_name, "value": max_count_unique_improvement_areas}
                )
                graph_3_data = sorted(graph_3_data, key=lambda x: x.get('value',0), reverse=True)
                        
            # this still a hard coded data we need to fix it later
            graph_2_data = [
                    {
                    "name": "Week 1",
                    "Finance": 40,
                    "Marketing": 24,
                    "Operations": 26,
                    "Hr": 10
                },
                {
                    "name": "Week 2",
                    "Finance": 30,
                    "Marketing": 30,
                    "Operations": 40,
                    "Hr": 20
                },
                {
                    "name": "Week 3",
                    "Finance": 20,
                    "Marketing": 10,
                    "Operations": 40,
                    "Hr": 30
                },
                {
                    "name": "Week 4",
                    "Finance": 10,
                    "Marketing": 20,
                    "Operations": 30,
                    "Hr": 20
                },
                {
                    "name": "Week 5",
                    "Finance": 40,
                    "Marketing": 30,
                    "Operations": 40,
                    "Hr": 20
                }
                ]
            
            graph_1_data = sorted(graph_1_data, key=lambda x: x['Participated'] + x['Not yet Participated'], reverse=True)
            graph_1 = {
                "name": "Departments wise participation",
                "data": graph_1_data
            }
            
            graph_2 = {
                "name": "Departments wise improvement rate",
                "data": graph_2_data
            }
            
            graph_3 = {
                "name": "Critical Improvement Areas",
                "data": graph_3_data
            }

            graph_4_data = []
            jd_interview_dict = {}
            for interview_tuple in jd_interviews_obj:
                jd_interview_obj = interview_tuple[0]
                report_json = jd_interview_obj.report_json
                
                if not report_json:
                    continue

                interview_graph_datas = report_json.get("graph_data")
                for interview_graph_data in interview_graph_datas:
                    if interview_graph_data["skill_name"] not in jd_interview_dict:
                        jd_interview_dict[interview_graph_data["skill_name"]] = [interview_graph_data["scored"]]

                    else:
                        jd_interview_dict[interview_graph_data["skill_name"]].append(interview_graph_data["scored"])
            

            for skill_name, scored_list in jd_interview_dict.items():
                graph_4_data.append(
                    {"skill_name": skill_name, "value": (sum(scored_list) / len(scored_list)) * 100}
                )
            

            graph_5_data = []
            cultural_interview_dict = {}
            for interview_tuple in cultural_interviews_obj:
                cultural_interview_obj = interview_tuple[0]
                report_json = cultural_interview_obj.report_json
                
                if not report_json:
                    continue

                interview_graph_datas = report_json.get("graph_data")
                for interview_graph_data in interview_graph_datas:
                    if interview_graph_data["skill_name"] not in cultural_interview_dict:
                        cultural_interview_dict[interview_graph_data["skill_name"]] = [interview_graph_data["scored"]]

                    else:
                        cultural_interview_dict[interview_graph_data["skill_name"]].append(interview_graph_data["scored"])
            

            for skill_name, scored_list in cultural_interview_dict.items():
                graph_5_data.append(
                    {"skill_name": skill_name, "value": (sum(scored_list) / len(scored_list)) * 10}
                )
                        
            graph_4 = {
                "name": "JD Interview skill overview",
                "data": graph_4_data
            }
            
            graph_5 = {
                "name": "Cultural Interview skill overview",
                "data": graph_5_data
            }
            
            
            response["graphs"] = [graph_1, graph_2, graph_3, graph_4, graph_5]
            return {"status": True, "data": response, "filters": filters}

        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def deep_analysis(self, analysis_mode, institution_id, filters):
        
        try:
            # based on filters pulling out list if users 
            
            role_obj = session.query(Role).filter_by(name = "Student").first()
            student_role_id = role_obj.id
                
            branch_id = None    
            branch_name = None
            if "branch" in filters:
                branch_name = filters["branch"].replace("+", " ")
                branch_obj = session.query(Branch).filter_by(name = branch_name).first()
                if branch_obj:
                    branch_id = branch_obj.id
                else:
                    branch_id, branch_name = self.default_branch_by_institution_id(institution_id)            
            else:
                branch_id, branch_name = self.default_branch_by_institution_id(institution_id)            

            filters["branch_id"] = branch_id
            filters["branch"] = branch_name

            course_id = None    
            course_name = None
            if "course" in filters:
                course_name = filters["course"].replace("+", " ")
                course_obj = session.query(Course).filter_by(name = course_name).first()
                course_id = None
                if course_obj:
                    course_id = course_obj.id
                else:
                    course_id, course_name = self.default_course_by_branch_id(branch_id)            
            else:
                course_id, course_name = self.default_course_by_branch_id(branch_id)

            filters["course_id"] = course_id
            filters["course"] = course_name

            department_id = None    
            department_name = None
            if "department" in filters:
                department_name = filters["department"].replace("+", " ")
                department_obj = session.query(Department).filter_by(name = department_name).first()
                if department_obj:
                    department_id = department_obj.id
                else:
                    department_id, department_name = self.default_department_by_course_id(course_id)
            else:
                department_id, department_name = self.default_department_by_course_id(course_id)
            
            filters["department_id"] = department_id
            filters["department"] = department_name

            interviews_obj = None
            unique_departments = {}

            if analysis_mode == 'ks_analysis':
                # requirement for this graph is 
                # Ks Analysis need to fix the logic Filters will be Branch and Course
                # Y axis: skill name 
                # X axis will be Department Names 
                # Cell logic is % of number of students certified in skill Vs Department
                # cerfified score limit is 7 (.env)

                user_obj = session.query(UserMaster.id,  UserMaster.certified_hard_skills, UserMaster.certified_soft_skills, Department.name).join(Department, UserMaster.department_id == Department.id).filter(UserMaster.role_id == student_role_id)
                
                # if department_id:
                #     user_obj = user_obj.filter(UserMaster.department_id == department_id)
                if course_id:
                    user_obj = user_obj.filter(UserMaster.course_id == course_id)
                elif branch_id:
                    user_obj = user_obj.filter(UserMaster.branch_id == branch_id)

                total_number_of_users = user_obj.count()
                user_obj = user_obj.all()
                
                filter_user_df = pd.DataFrame(user_obj, columns=["user_id", "certified_hard_skills", "certified_soft_skills", "name"])
                print("--------------------")
                print("filter_user_df \n", filter_user_df)
                filter_user_df['certified_hard_skills'] = filter_user_df['certified_hard_skills'].apply(lambda x: x if isinstance(x, str) else "")
                filter_user_df['certified_soft_skills'] = filter_user_df['certified_soft_skills'].apply(lambda x: x if isinstance(x, str) else "")
                
                unique_department_names = list(set([row[3] for row in user_obj]))

                ks_analysis_graph_data_hard_skills = []
                ks_analysis_graph_data_soft_skills = []

                user_obj = session.query(UserMaster.id,  UserMaster.certified_hard_skills, UserMaster.certified_soft_skills, Department.name).join(Department, UserMaster.department_id == Department.id).filter(UserMaster.role_id == student_role_id)
                department_obj = session.query(InstitutionMaster.institution_name, Department.name) \
                        .join(InstitutionBranchMapping, InstitutionMaster.id == InstitutionBranchMapping.institution_id) \
                        .join(BranchCourseMapping, BranchCourseMapping.branch_id == InstitutionBranchMapping.branch_id) \
                        .join(CourseDepartmentMapping, CourseDepartmentMapping.course_id == BranchCourseMapping.course_id) \
                        .join(Branch, BranchCourseMapping.branch_id == Branch.id) \
                        .join(Course, CourseDepartmentMapping.course_id == Course.id) \
                        .join(Department, CourseDepartmentMapping.department_id == Department.id) \
                        .filter(InstitutionMaster.id == institution_id) \
                        .filter(Branch.id == branch_id) \
                        .filter(Course.id == course_id) \
                        .all()
                unique_department_names = list(set([item[1] for item in department_obj]))
                
                unique_hard_skills_obj = session.query(InstitutionMaster.institution_name, HardSkill.name) \
                    .join(InstitutionHardSkillMapping, InstitutionMaster.id == InstitutionHardSkillMapping.institution_id) \
                    .join(HardSkill, HardSkill.id == InstitutionHardSkillMapping.skill_id) \
                    .filter(InstitutionMaster.id == institution_id).all()
                unique_hard_skill_dict = {item[1]:0 for item in unique_hard_skills_obj}
                
                unique_soft_skills_obj = session.query(InstitutionMaster.institution_name, SoftSkill.name) \
                    .join(InstitutionSoftSkillMapping, InstitutionMaster.id == InstitutionSoftSkillMapping.institution_id) \
                    .join(SoftSkill, SoftSkill.id == InstitutionSoftSkillMapping.skill_id) \
                    .filter(InstitutionMaster.id == institution_id).all()
                unique_soft_skill_dict = {item[1]:0 for item in unique_soft_skills_obj}


                for unique_department_name in unique_department_names:
                    filtered_df = filter_user_df[filter_user_df['name'] == unique_department_name]
                    temp_unique_hard_skill_dict = unique_hard_skill_dict
                    temp_unique_soft_skill_dict = unique_soft_skill_dict
                    for index, row in filtered_df.iterrows():
                        for hard_skill in row['certified_hard_skills'].split(','):
                            if hard_skill in temp_unique_hard_skill_dict:
                                temp_unique_hard_skill_dict[hard_skill] += 1
                            else:
                                temp_unique_hard_skill_dict[hard_skill] = 1
                        for soft_skill in row['certified_soft_skills'].split(','):
                            if soft_skill in temp_unique_soft_skill_dict:
                                temp_unique_soft_skill_dict[soft_skill] += 1
                            else:
                                temp_unique_soft_skill_dict[soft_skill] = 1
                            
                    
                    temp_unique_hard_skill_dict.pop("", None)
                    temp_unique_soft_skill_dict.pop("", None)

                    hard_skills_extended_list = []
                    for skill in temp_unique_hard_skill_dict:
                        try:
                            hard_skills_extended_list.append({"x": skill, "y": round((temp_unique_hard_skill_dict[skill]/total_number_of_users)*100, 2)})
                        except ZeroDivisionError:
                            hard_skills_extended_list.append({"x": skill, "y": 0})
                
                    soft_skills_extended_list = []
                    for skill in temp_unique_soft_skill_dict:
                        try:
                            soft_skills_extended_list.append({"x": skill, "y": round((temp_unique_soft_skill_dict[skill]/total_number_of_users)*100, 2)})
                        except ZeroDivisionError:
                            soft_skills_extended_list.append({"x": skill, "y": 0})

                    ks_analysis_graph_data_hard_skills.append({
                        "id": unique_department_name,
                        "data": hard_skills_extended_list
                    })
                    ks_analysis_graph_data_soft_skills.append({
                        "id": unique_department_name,
                        "data": soft_skills_extended_list
                    })
                                        
                ks_analysis_graph = {
                    "status": True,
                    "name": "Knowledge and Skill Analysis",
                    "filters": filters,
                    "data": {
                        "graph_1":{
                            "name": "Hard skills",
                            "data": ks_analysis_graph_data_hard_skills
                        },
                        "graph_2":{
                            "name": "Soft skills",
                            "date": ks_analysis_graph_data_soft_skills
                        }
                    }
                }
                return ks_analysis_graph
            
            elif analysis_mode == 'practical_thinking_analysis':
                practical_thinking_analysis_graph_data = []
                
                # if 'department' in filters:    
                #     unique_departments_obj = session.query(Department).filter_by(id = department_id).first()
                #     unique_departments = {unique_departments_obj.id: unique_departments_obj.name}
            
                if 'course' in filters:
                    unique_departments_obj = session.query(Department.id, Department.name)\
                    .join(CourseDepartmentMapping, Department.id == CourseDepartmentMapping.department_id)\
                    .filter(CourseDepartmentMapping.course_id == course_id)\
                    .distinct()
                    unique_departments = {row[0]:row[1] for row in unique_departments_obj.all()}
                
                elif 'branch'in filters:
                    course_ids_obj = session.query(BranchCourseMapping.course_id)\
                    .filter(BranchCourseMapping.branch_id == branch_id)\
                    .all()
                    course_ids = [row[0] for row in course_ids_obj]
                    
                    unique_departments_obj = session.query(Department.id, Department.name)\
                    .join(CourseDepartmentMapping, Department.id == CourseDepartmentMapping.department_id)\
                    .filter(CourseDepartmentMapping.course_id.in_(course_ids))\
                    .distinct()
                    unique_departments = {row[0]:row[1] for row in unique_departments_obj.all()}
                
                else:
                    branch_ids_obj = session.query(InstitutionBranchMapping.branch_id)\
                        .filter(InstitutionBranchMapping.institution_id == institution_id)\
                        .all()
                    branch_ids = [row[0] for row in branch_ids_obj]

                    course_ids_obj = session.query(BranchCourseMapping.course_id)\
                        .filter(BranchCourseMapping.branch_id.in_(branch_ids))\
                        .all()
                    course_ids = [row[0] for row in course_ids_obj] 
                                    
                    unique_departments_obj = session.query(Department.id, Department.name)\
                        .join(CourseDepartmentMapping, Department.id == CourseDepartmentMapping.department_id)\
                        .filter(CourseDepartmentMapping.course_id.in_(course_ids))\
                        .distinct()  

                    unique_departments = {row[0]:row[1] for row in unique_departments_obj.all()}
                                
                filtered_department_ids = list(set(unique_departments.keys())) 
                filtered_department_names = list(set(unique_departments.values()))
            
                for filtered_department_id in filtered_department_ids:
                    relevant_answers = 0
                    un_relevant_answers = 0
                    user_obj = session.query(UserMaster.id).filter_by(department_id = filtered_department_id).filter_by(role_id = student_role_id).all()
                    user_ids = [row[0] for row in user_obj]
                    filter_interviews = session.query(InterviewMaster).filter(InterviewMaster.user_id.in_(user_ids)).all()  
                    
                    for filter_interview in filter_interviews:
                        if filter_interview.relevant_answers:
                            relevant_answers = relevant_answers + filter_interview.relevant_answers
                        
                        if filter_interview.un_relevant_answers:
                            un_relevant_answers = un_relevant_answers + filter_interview.un_relevant_answers
                    practical_thinking_analysis_graph_data.append({
                    "Not Solved": un_relevant_answers,
                    "Solved": relevant_answers,
                    "name": unique_departments[filtered_department_id],
                    })
                
                practical_thinking_graph = {
                "status": True,
                "name": "Practical Thinking", 
                "filters": filters,
                "data": practical_thinking_analysis_graph_data
                }
                return practical_thinking_graph
            
            elif analysis_mode == 'emotion_sensing':
                if "start_date" in filters:
                    start_date = filters["start_date"]
                    end_date = filters["end_date"]
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')

                else:
                    current_date = datetime.now()
                    end_date = current_date + timedelta(days=1)
                    start_date = current_date - timedelta(days=7)
                    filters["start_date"] = start_date.strftime("%Y-%m-%d")
                    filters["end_date"] = end_date.strftime("%Y-%m-%d")

                student_id = filters.get("student_id")
                if not student_id:
                    session.query(UserMaster)
                    temp_user = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(role_id = student_role_id).filter_by(department_id = department_id).first()
                    if temp_user:
                        student_id = temp_user.id
                        student_name = temp_user.first_name + temp_user.last_name
                    else:
                        student_id = 0
                        student_name = ""
                else:
                    student_obj = session.query(UserMaster).filter_by(id = student_id).first()
                    student_name = student_obj.first_name + student_obj.last_name

                interviews_obj = session.query(InterviewMaster).filter_by(user_id = student_id).filter_by(status = 'report_generated').filter(InterviewMaster.created_date >= start_date, InterviewMaster.created_date < end_date).all()
            
                positive_emotions_graph_data = []
                neutral_emotions_graph_data = []
                negative_emotions_graph_data = []
                
                count = 1
                for interview in interviews_obj:
                    ds_result_json = interview.result_json
                    emotion_count = ds_result_json.get("Emotion count", {})
                    if isinstance(emotion_count, str):
                        emotion_count = json.loads(emotion_count)

                    emotion_count = {key: float(value) for key, value in emotion_count.items()}
                    positive_emotions_graph_data.append({"name": count, "Happiness": emotion_count.get("happy", 0)})
                    neutral_emotions_graph_data.append({"name": count, "Suprise": emotion_count.get("surprise", 0)})
                    negative_emotions_graph_data.append({
                        "name": count, 
                        "Disgust": emotion_count.get("disgust", 0),
                        "Contempt": emotion_count.get("disgust", 0),
                        "Sadness": emotion_count.get("sad", 0),
                        "Anger": emotion_count.get("angry", 0),
                        "Fear": emotion_count.get("fear", 0)
                    })
                    count = count + 1
                
                filters["user_id"] = student_id
                filters["user_name"] = student_name

                emotion_sensing_graph = {
                    "status": True,
                    "name": "Emotion Sensing", 
                    "filters": filters,
                    "data": {
                        "graph_1": {
                        "name": "Positive Emotions",
                        "data": positive_emotions_graph_data
                        },
                        "graph_2": {
                        "name": "Neutral Emotions",
                        "data": neutral_emotions_graph_data
                        },
                        "graph_3": {
                        "name": "Negative Emotions",
                        "data": negative_emotions_graph_data
                        }
                    }
                }                
                return emotion_sensing_graph
            
            else:
                return {"status": True, "data": {}, "filters": filters}
            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def upload_configurations(self,institution_id, data):
        try:
            blob = data.get("base64")
            mode = data.get("mode")
            
            if not mode:
                return {"status": False, "message": "invalid configaration request"}
            
            if not blob:
               return {"status": False, "message": "invalid configaration file"} 
            
            mode = str(mode).strip().lower().replace(" ", "_")
            print("mode", mode)
            
            institution_obj = session.query(InstitutionMaster).filter_by(id = institution_id).first()
            institution_name = institution_obj.institution_name
            configaration_version = institution_obj.configuration_version
            if not configaration_version:
                configaration_version = {}
            file_version = configaration_version.get(mode, 0) + 1
            configaration_version[mode] = file_version
            
            new_record = ConfigurationHistory(
                category = mode,
                version = file_version,
                created_by = institution_id,
                status = 'inprogress'
            )
            session.add(new_record)
            session.commit()
            
            file_data = base64.b64decode(blob)
            file_data_name = f'uploaded_file_{institution_id}_{mode}.xlsx'
                
            with open(file_data_name, 'wb') as file:
                file.write(file_data)
            
            data_df = pd.read_excel(file_data_name, engine='openpyxl')
            # data_df_columns = data_df.columns.tolist()
            
            if mode == 'hard_skill':
                current_skills_details = self.hard_skills_list(institution_id = institution_id)
                current_skills = [h.get('name', "") for h in current_skills_details]
                if data_df.empty:
                    data_df = pd.DataFrame(columns = ['Name'])
                data_df = data_df.dropna(subset=['Name'])
                requested_skills = data_df['Name'].tolist()
                new_skills, deleted_skills, unchanged_skills = identify_list_differences(current_skills, requested_skills)
                
                print()
                print("Hard skills")
                print("current_skills", current_skills)
                print("requested_skills", requested_skills)
                print("new_skills", new_skills)
                print("deleted_skills", deleted_skills)
                print()
    
                for new_skill in new_skills:
                    skill_id = self.create_hard_skills(new_skill)
                    self.create_hard_skills_mapping(institution_id, institution_name, skill_id, new_skill)
                    generate_skill_improvement_suggestions(new_skill, mode)
                    generate_skill_questions(new_skill, mode)
                    
                for deleted_skill in deleted_skills:
                    skill_id = self.create_hard_skills(deleted_skill)
                    self.delete_hard_skills_mapping(institution_id, institution_name, skill_id, deleted_skill)
                    
            elif mode == 'soft_skill':
                current_skills_details = self.soft_skills_list(institution_id=institution_id)
                current_skills = [h.get('name', "") for h in current_skills_details]
                if data_df.empty:
                    data_df = pd.DataFrame(columns = ['Name'])
                
                data_df = data_df.dropna(subset=['Name'])
                requested_skills = data_df['Name'].tolist()
                new_skills, deleted_skills, unchanged_skills = identify_list_differences(current_skills, requested_skills)
                
                print()
                print("Soft skills")
                print("current_skills", current_skills)
                print("requested_skills", requested_skills)
                print("new_skills", new_skills)
                print("deleted_skills", deleted_skills)
                print()
                
                
                for new_skill in new_skills:
                    skill_id = self.create_soft_skills(new_skill)
                    self.create_soft_skills_mapping(institution_id, institution_name, skill_id, new_skill)
                    generate_skill_improvement_suggestions(new_skill, 'soft_skill')
                    generate_skill_questions(new_skill, 'soft_skill')
                    
                for deleted_skill in deleted_skills:
                    skill_id = self.create_hard_skills(deleted_skill)
                    self.delete_soft_skills_mapping(institution_id, institution_name, skill_id, deleted_skill)
                    
            elif mode == 'company':
                if data_df.empty:
                    data_df = pd.DataFrame(columns = ['Company', 'Position'])
                df_cleaned = data_df.dropna(subset=['Company', 'Position'])
                requested_company_details = df_cleaned.groupby('Company')['Position'].apply(list).to_dict()
                company_details = self.companies_list(institution_id=institution_id)
                current_company_details = {}
                for current_company in company_details:             
                    current_company_name = current_company.get('name')
                    current_company_role_ids_str = current_company.get('role_ids', "")
                    current_company_role_ids = current_company_role_ids_str.split(",")
                    current_company_role_names = self.get_interview_roles_list_names(current_company_role_ids)
                    current_company_details[current_company_name] = current_company_role_names
                new_companies, deleted_companies, unchanged_companies = identify_list_differences(current_company_details.keys(), requested_company_details.keys())

                print()
                print("Companies")
                print("current_company_details", current_company_details)
                print("requested_company_details", requested_company_details)
                print("new_companies", new_companies)
                print("deleted_companies", deleted_companies)
                print("unchanged_companies", unchanged_companies)
                print()

                for new_company in new_companies:
                    company_id = self.create_new_company(new_company)
                    print("company_id", company_id)
                    company_role_ids_list = self.get_interview_roles_list_ids(requested_company_details[new_company])
                    company_role_ids_str = ','.join(list(map(str,company_role_ids_list)))
                    self.create_company_mapping(institution_id, company_id, company_role_ids_str, new_company)
                    # generate_company_questions(new_company, requested_company_details[new_company])
                    
                for deleted_company in deleted_companies:
                    company_id = self.create_new_company(deleted_company)
                    self.delete_company_mapping(institution_id, company_id, deleted_company)

                for unchanged_company in unchanged_companies:
                    company_id = self.create_new_company(unchanged_company)
                    company_role_ids_list = self.get_interview_roles_list_ids(requested_company_details[unchanged_company])
                    company_role_ids_str = ','.join(list(map(str, company_role_ids_list)))
                    self.create_company_mapping(institution_id, company_id, company_role_ids_str, unchanged_company)
                    # generate_company_questions(unchanged_companie, requested_company_details[unchanged_companie])

            elif mode == 'institution':
                data_df = data_df.dropna(subset=['Branch', 'Course', 'Department'])
                requested_institution_details = {}
                for index, row in data_df.iterrows():
                    branch = row['Branch']
                    course = row['Course']
                    department = row['Department']
                    if branch not in requested_institution_details:
                        requested_institution_details[branch] = {}
                    if course not in requested_institution_details[branch]:
                        requested_institution_details[branch][course] = []
                    requested_institution_details[branch][course].append(department)
                
                institution_details = self.get_institution_config(institution_id=institution_id)
                institution_details_df = pd.DataFrame.from_dict(institution_details)
                institution_details_df.rename(columns={'branch_name': 'Branch', 'course_name': 'Course', 'department_name': 'Department'}, inplace=True)
                print("institution_details_df", institution_details_df)
                if institution_details_df.empty:
                    institution_details_df = pd.DataFrame(columns=['Branch', 'Course', 'Department'])

                institution_details_df = institution_details_df.dropna(subset=['Branch', 'Course', 'Department'])
                
                current_institution_details = {}
                
                for index, row in institution_details_df.iterrows():
                    branch = row['Branch']
                    course = row['Course']
                    department = row['Department']
                    if branch not in current_institution_details:
                        current_institution_details[branch] = {}
                    if course not in current_institution_details[branch]:
                        current_institution_details[branch][course] = []
                    current_institution_details[branch][course].append(department)
                               
                new_branchs, deleted_branchs, unchanged_branchs = identify_list_differences(current_institution_details.keys(), requested_institution_details.keys())
                        
                print()
                print("Branch details for institution", institution_name)
                print("current_branchs", current_institution_details.keys())
                print("requested_branchs", requested_institution_details.keys())
                print("new_branchs", new_branchs)
                print("deleted_branchs", deleted_branchs)
                print("unchanged_branchs", unchanged_branchs)
                print()

                for branch_name in new_branchs:
                    branch_id = self.create_branch(branch_name)
                    self.create_institution_branch_mapping(institution_id, branch_id, institution_name, branch_name)
                
                for branch_name in deleted_branchs:
                    branch_id = session.query(Branch).filter_by(name = branch_name).first().id
                    self.delete_institution_branch_mapping(institution_id, branch_id, institution_name, branch_name)

                requested_branchs = list(new_branchs) + list(unchanged_branchs) 
                        
                for branch_name in requested_branchs:
                    current_branch_details = current_institution_details.get(branch_name, {})
                    requested_branch_details = requested_institution_details[branch_name]
                    
                    branch_id = session.query(Branch).filter_by(name = branch_name).first().id
                    new_courses, deleted_courses, unchanged_courses = identify_list_differences(current_branch_details.keys(), requested_branch_details.keys())
                    
                    print()
                    print("course details for branch", branch_name)
                    print("current_course", current_branch_details.keys())
                    print("requested_course", requested_branch_details.keys())
                    print("new_courses", new_courses)
                    print("deleted_courses", deleted_courses)
                    print("unchanged_courses", unchanged_courses)
                    print()
                    
                    for course_name in new_courses:
                        course_id = self.create_course(course_name)
                        self.create_branch_course_mapping(branch_id, course_id, branch_name, course_name) # Harnath
                    
                    for course_name in deleted_courses:
                        course_id = session.query(Course).filter_by(name = course_name).first().id
                        self.delete_branch_course_mapping(branch_id, course_id, branch_name, course_name)
                    
                    requested_courses = list(new_courses) + list(unchanged_courses)
                    current_courses = current_branch_details.keys() 
                    
                    for course_name in requested_courses:
                        current_courses_details =  current_branch_details.get(course_name, )
                        
                        course_id = session.query(Course).filter_by(name = course_name).first().id
                        new_departments, deleted_departments, unchanged_departments = identify_list_differences(current_branch_details.get(course_name, []), requested_branch_details.get(course_name, []))

                        print()
                        print("Departments data for course", course_name)
                        print("current_departments", current_branch_details.get(course_name, []))
                        print("requested_departments", requested_branch_details.get(course_name, []))
                        print("new_departments", new_departments)
                        print("deleted_departments", deleted_departments)
                        print("unchanged_departments", unchanged_departments)
                        print()

                        for department_name in new_departments:
                            department_id = self.create_department(department_name)
                            self.create_course_department_mapping(course_id, department_id, course_name, department_name)

                        for department_name in deleted_departments:
                            department_id = session.query(Department).filter_by(name = department_name).first().id
                            self.delete_course_department_mapping(course_id, department_id, course_name, department_name)
            
            elif mode == 'interview_questions':
                skill_based_questions_df = pd.read_excel(file_data_name, sheet_name='Skill Based Questions')
                company_based_questions_df = pd.read_excel(file_data_name, sheet_name='Company Based Questions')

                print("Strated processing skill based interview questions")
                temp_hard_skill_dict = {}
                temp_soft_skill_dict = {}
                print("skill_based_questions_df", skill_based_questions_df)
                for index, row in skill_based_questions_df.iterrows():
                    category = str(row['Category']).strip().lower().replace(' ', '_')
                    level = str(row['Level']).strip().lower().replace(' ', '_')
                    skill_name = row['Skill Name']
                    question = row['Question']
                    
                    if category not in ["hard_skill", "soft_skill"]:
                        print("for the following row category is invalid")
                        print("Row", row)
                        continue
                    if level not in ["beginner", "intermediate", "expert"]:
                        print("for the following row level is invalid")
                        print("Row", row)
                        continue

                    if category == "hard_skill":
                        if skill_name in temp_hard_skill_dict:
                            if level in temp_hard_skill_dict[skill_name]:
                                temp_hard_skill_dict[skill_name][level].append(question)
                            else:
                                temp_hard_skill_dict[skill_name][level] = [question]
                        else:
                            skill_id = self.create_hard_skills(skill_name)
                            self.create_hard_skills_mapping(institution_id, institution_name,skill_id, skill_name)                           
                            generate_skill_improvement_suggestions(skill_name, category)
                            generate_skill_questions(skill_name, category)
                            temp_hard_skill_dict[skill_name] = {}
                            temp_hard_skill_dict[skill_name]["skill_id"] = skill_id
                            temp_hard_skill_dict[skill_name][level] = [question]

                            # print("---------------------------")
                            # print("skill_name", skill_name)
                            # print("institution_id", institution_id)
                            # print('temp_hard_skill_dict[skill_name].get("beginner", [])', temp_hard_skill_dict[skill_name].get("beginner", []))
                            # print('temp_hard_skill_dict[skill_name].get("intermediate", [])', temp_hard_skill_dict[skill_name].get("intermediate", []))
                            # print('temp_hard_skill_dict[skill_name].get("expert", [])', temp_hard_skill_dict[skill_name].get("expert", []))                            
                            # print("---------------------------")

                    elif category == "soft_skill":
                        if skill_name in temp_soft_skill_dict:
                            if level in temp_soft_skill_dict[skill_name]:
                                temp_soft_skill_dict[skill_name][level].append(question)
                            else:
                                temp_soft_skill_dict[skill_name][level] = [question]
                        else:
                            skill_id = self.create_soft_skills(skill_name)
                            self.create_soft_skills_mapping(institution_id, skill_id, skill_name)
                            generate_skill_improvement_suggestions(skill_name, category)
                            generate_skill_questions(skill_name, category)
                            temp_soft_skill_dict[skill_name] = {}
                            temp_soft_skill_dict[skill_name]["skill_id"] = skill_id
                            temp_soft_skill_dict[skill_name][level] = [question]

                            
                # print("temp_hard_skill_dict", temp_hard_skill_dict)
                # print("temp_soft_skill_dict", temp_soft_skill_dict)

                for skill_name in temp_hard_skill_dict:
                    # skill_custom_questions = HardSkillCustomQuestions(
                    #     name=skill_name, 
                    #     institution_id = institution_id,
                    #     beginner=temp_hard_skill_dict[skill_name].get("beginner", []),
                    #     intermediate=temp_hard_skill_dict[skill_name].get("intermediate", []),
                    #     expert=temp_hard_skill_dict[skill_name].get("expert", [])
                    # )
                    # skill_custom_questions.save()
                    HardSkillCustomQuestions.objects(name=skill_name, institution_id=institution_id).update_one(
                        set__beginner=temp_hard_skill_dict[skill_name].get("beginner", []),
                        set__intermediate=temp_hard_skill_dict[skill_name].get("intermediate", []),
                        set__expert=temp_hard_skill_dict[skill_name].get("expert", []),
                        upsert=True
                    )        
                
                for skill_name in temp_soft_skill_dict:
                    # skill_custom_questions = SoftSkillCustomQuestions(
                    #     name=skill_name, 
                    #     institution_id = institution_id,
                    #     beginner=temp_soft_skill_dict[skill_name].get("beginner", []),
                    #     intermediate=temp_soft_skill_dict[skill_name].get("intermediate", []),
                    #     expert=temp_soft_skill_dict[skill_name].get("expert", [])
                    # )
                    # skill_custom_questions.save()
                    SoftSkillCustomQuestions.objects(name=skill_name, institution_id=institution_id).update_one(
                        set__beginner=temp_soft_skill_dict[skill_name].get("beginner", []),
                        set__intermediate=temp_soft_skill_dict[skill_name].get("intermediate", []),
                        set__expert=temp_soft_skill_dict[skill_name].get("expert", []),
                        upsert=True
                    )
    
                print("Completed processing skill based interview questions")
                print("Strated processing company based interview questions")

                level_filters = ["beginner", "intermediate", "expert"]
                
                company_based_questions_df = company_based_questions_df[company_based_questions_df['Level'].isin(level_filters)]
                
                company_grouped_df = company_based_questions_df.groupby('Company Name')
                
                temp_company_role_dict = {}
                for company_name, company_group_df in company_grouped_df:
                    temp_company_role_dict[company_name] = {}
                    company_id = self.create_new_company(company_name)
                    company_roles = list(set(company_group_df['Role'].tolist()))
                    company_roles_ids = []
                    for company_role in company_roles:
                        company_roles_id = self.create_working_roles(company_role)
                        if company_roles_id:
                            company_roles_ids.append(company_roles_id)
                    self.create_company_mapping(institution_id, company_id, company_roles_ids, company_name)

                    for index, row in company_group_df.iterrows():
                        level = str(row['Level']).strip().lower().replace(' ', '_')
                        working_role = row['Role']
                        question = row['Question']
                        tag = row["Tag"]

                        if working_role in temp_company_role_dict[company_name]:
                            if level in temp_company_role_dict[company_name][working_role][level]:
                                if tag in temp_company_role_dict[company_name][working_role][level]:
                                    temp_company_role_dict[company_name][working_role][level][tag].append(question)
                                else:
                                    temp_company_role_dict[company_name][working_role][level][tag] = [question]              
                            else:
                                temp_company_role_dict[company_name][working_role][level] = {}
                                temp_company_role_dict[company_name][working_role][level][tag] = [question]
                        else:
                            temp_company_role_dict[company_name][working_role] = {}
                            temp_company_role_dict[company_name][working_role][level] = {}
                            temp_company_role_dict[company_name][working_role][level][tag] = [question]
                                
                for company_name in temp_company_role_dict:
                    for company_role_name in temp_company_role_dict[company_name]:
                        CompanyRoleCustomQuestions.objects(company = company_name, role_name = company_role_name, institution_id = institution_id).update_one(
                            set__beginner=temp_company_role_dict[company_name][company_role_name].get("beginner", []),
                            set__intermediate=temp_company_role_dict[company_name][company_role_name].get("intermediate", []),
                            set__expert=temp_company_role_dict[company_name][company_role_name].get("expert", []),
                            upsert=True
                        )
                print("Completed processing company based interview questions")

            elif mode == 'placment_tracker':
                if data_df.empty:
                    return {"status": False, "message": "No data found"}
                df_columns = data_df.columns
                for column in df_columns:
                    if column not in UPLOAD_USER_FILE_PLACEMENT_TRACKER_HEADERS:
                        return {"status":  False, "message": "Invalid headers found"}
                
                placement_objs = session.query(PlacementDetails.user_id, UserMaster.student_id.label('student_id'))\
                    .join(UserMaster, UserMaster.id == PlacementDetails.user_id)\
                    .filter_by(institution_id = institution_id).all()
                
                placed_student_mapping = {
                    placement_obj.student_id: placement_obj.user_id for placement_obj in placement_objs}     
                
                
                for index, row in data_df.iterrows():
                    student_id = row["Student ID"]
                    if student_id in placed_student_mapping:
                        update_stmt = (
                        update(PlacementDetails).
                        where(PlacementDetails.user_id == placed_student_mapping[student_id]).
                        values(
                            status= row["Status"],
                            company_name= row["Company Name"],
                            company_type= row["Company Type"],
                            offer= row["Offer"],
                            offer_type= row["Offer Type"]
                            )
                        )
                        session.execute(update_stmt)
                        session.commit() 

                    else:
                        new_record = PlacementDetails(
                            user_id = placed_student_mapping[student_id],
                            status= row["Status"],
                            company_name= row["Company Name"],
                            company_type= row["Company Type"],
                            offer= row["Offer"],
                            offer_type= row["Offer Type"]
                        )
                        session.add(new_record)
                        session.commit()

            elif mode == 'question': 
                list_of_dicts = data_df.to_dict(orient='records')
                return_data = []
                for item in list_of_dicts:
                    options = [item["Option1"], item["Option2"], item["Option3"], item["Option4"]]
                    correct_answers = item["Correct Options"].split(",")
                    correct_options = []
                    for correct_answer in correct_answers:
                        correct_options.append(options.index(correct_answer) + 1) 
                    
                    return_data.append({
                        "question": item["Question"],
                        "answerType": item["Answer Type"],
                        "marks": item["Marks"],
                        "options": options,
                        "numberOfOptions": len(options),
                        "correctAnswer": correct_options
                    })                
                return {"status": True, "data": return_data}

            else:
               return {"status": False, "message": "invalid configaration request"} 
            
            google_drive_object =  GoogleDriveManager()
            configaration_file_name = f"{mode}_{file_version}.xlsx"
            
            # checking folder for that institution
            print("institution_name", institution_name)
            institution_based_folder = google_drive_object.folder_exists_by_name(institution_name)
            institution_based_folder_id = institution_based_folder.get('id')
            print("institution folder id", institution_based_folder_id)
            if not institution_based_folder_id:
                institution_based_folder_id = google_drive_object.create_folder(institution_name)

            file_details = google_drive_object.create_file(configaration_file_name, institution_based_folder_id, file_data_name)
            print("file_details", file_details)
            file_details_id = file_details["id"]

            institution_obj.configuration_version = configaration_version
            new_record.status = 'completed'
            new_record.details = {"google_file_id": file_details_id}
            session.commit()
            print(f"Configuration updated for {new_record.id}")

            try:
                os.remove(file_data_name)
            except OSError as e:
                print(f"Error: {file_data_name} : {e.strerror}")
            
        except Exception as e:
            traceback.print_exc()
            new_record.status = 'error'
            new_record.error = str(e)
            session.commit()
            return {"status": False, "message": "error", "error": str(e)}
    
    def download_configurations(self, institution_id, mode):
        try:
            institution_obj = session.query(InstitutionMaster).filter_by(id = institution_id).first()
            institution_name = institution_obj.institution_name
            if institution_obj:
                mode = str(mode).strip().lower().replace(" ", "_")
                if mode == 'placement_tracker':
                    user_obj = session.query(
                        UserMaster.id.label('id'),
                        UserMaster.student_id,
                        UserMaster.first_name,
                        UserMaster.last_name,
                        Department.name.label('department_name'),
                        func.coalesce(PlacementDetails.status, 'Not Placed').label('status'),
                        PlacementDetails.company_name,
                        PlacementDetails.company_type,
                        PlacementDetails.offer,
                        PlacementDetails.offer_type
                    )\
                    .join(Role, UserMaster.role_id == Role.id)\
                    .join(Department, UserMaster.department_id == Department.id)\
                    .outerjoin(PlacementDetails, UserMaster.id == PlacementDetails.user_id)\
                    .filter(UserMaster.institution_id == institution_id)\
                    .filter(Role.name == 'Student').all()

                    wb = Workbook()
                    ws = wb.active
                    ws.title = "Student Data"
                    ws.freeze_panes = 'F1'  # Freezes the first five columns
                    ws.append(UPLOAD_USER_FILE_PLACEMENT_TRACKER_HEADERS)
                    for user in user_obj:
                        print("user", user)
                        ws.append([
                            user.id,
                            user.student_id,
                            user.first_name,
                            user.last_name,
                            user.department_name,
                            user.status,
                            user.company_name,
                            user.company_type,
                            user.offer,
                            user.offer_type
                        ])

                    local_path = f'{institution_name}_{mode}.xlsx'
                    wb.save(local_path)
                    return {"status": True, "file_name": local_path}    
                
                if mode == 'question':
                    return {"status": False, "file_name": ""}
                
                configaration_version = institution_obj.configuration_version
                if configaration_version:
                    file_version_number = configaration_version.get(mode, 0)
                else:
                    file_version_number = 0
                configaration_history_obj = session.query(ConfigurationHistory).filter_by(category = mode).filter_by(version = str(file_version_number)).first()
                google_drive_id = configaration_history_obj.details.get("google_file_id")
                local_path = f"{institution_id}_{mode}_{file_version_number}.xlsx"
                
                google_drive_object =  GoogleDriveManager()
                google_drive_object.download_file(google_drive_id, local_path)

                return {"status": True, "file_name": local_path}            
            else:
                return {"status": False, "message": "institution not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        
    def generate_screening_link(self, data, institution_id):
        try:
            unique_code = str(uuid.uuid4())
            screening = ScreeningMaster(
                name=data["name"], 
                description=data.get("description", ""), 
                max_capacity = data.get("max_capacity", 0),
                activation_date = data["activation_date"],
                expiry_date = data["expiry_date"],
                unique_code=unique_code,
                created_by = institution_id,
                updated_by = institution_id,
                is_active = True
                )
            session.add(screening)
            session.commit()
            return {"screening_code": unique_code, "screening_id": screening.id,"status": True, "message": "screening link created"}
                        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        
    def screening_link_list(self, institution_id):
        try:
            screening_list = session.query(ScreeningMaster).filter_by(created_by = institution_id).order_by(desc(ScreeningMaster.id)).all()
            return {"status": True, "data": obj_to_list(screening_list)}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def screening_active(self, screening_code):
        try:
            screening_obj = session.query(ScreeningMaster).filter_by(unique_code = screening_code).first()
            if screening_obj:
                screening_obj.is_active = True
                session.commit()
                return {"status": True, "meassage": "screening activated"}
            else:
                return {"status": False, "message": "screening not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    
    def screening_deactive(self, screening_code):
        try:
            screening_obj = session.query(ScreeningMaster).filter_by(unique_code = screening_code).first()
            if screening_obj:
                screening_obj.is_active = False
                session.commit()
                return {"status": True, "meassage": "screening deactivated"}
            else:
                return {"status": False, "message": "screening not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    def screening_user_list(self, screening_code, column_name='created_date', order_by='DESC', page_number=1, limit=20):
        try:
            mode = "Screening"
            users = session.query(
                                UserMaster.first_name,
                                UserMaster.last_name,
                                UserMaster.number_of_interviews,
                                UserMaster.id,
                                UserMaster.phone_number,
                                UserMaster.address,
                                UserMaster.email,
                                UserMaster.created_date,
                                UserMaster.is_active,
                                UserMaster.screening_id,
                                ScreeningMaster.unique_code.label("screening_code"),
                                Branch.name.label("branch_name"), 
                                Department.name.label("department_name"),
                                Course.name.label("course_name")) \
                .join(Role, UserMaster.role_id == Role.id) \
                .join(Branch, UserMaster.branch_id == Branch.id) \
                .join(Department, UserMaster.department_id == Department.id) \
                .join(Course, UserMaster.course_id == Course.id)\
                .join(ScreeningMaster, UserMaster.screening_id == ScreeningMaster.id)\
                .filter(Role.name == mode)\
                .filter(ScreeningMaster.unique_code == screening_code) 
                
            if order_by == 'DESC':
                users = users.order_by(desc(getattr(UserMaster, column_name))).all()
            else:
                users = users.order_by(asc(getattr(UserMaster, column_name))).all()
            
            data_list = []
            for user in users:
                student_id = user.id
                interviews_data = session.query(InterviewMaster.percentage).filter_by(status = 'report_generated').filter_by(user_id = student_id).all()
                scorelist = []
                for item in interviews_data:
                    if item[0] is None:
                        scorelist.append(0)
                    else:
                        try:
                            scorelist.append(round(item[0],2))
                        except:
                            scorelist.append(0)
                
                average = sum(scorelist) / len(scorelist) if scorelist else 0
                data_list.append(   
                {
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}",
                    "phone_number": user.phone_number,
                    "address": user.address,
                    "email": user.email,
                    "branch_name": user.branch_name,
                    "department_name": user.department_name,
                    "avg_score": round(average,2),
                    "course_name": user.course_name,
                    "created_date": str(user.created_date),
                    "is_active": user.is_active,
                    "screening_id": user.screening_id,
                    "screening_code": user.screening_code
                })
            
            if data_list:
                total_records = len(data_list)
                print("total_records", total_records)
                total_pages = (total_records + limit - 1) // limit
                start_index = (page_number - 1) * limit
                end_index = start_index + limit
                print("limit", limit)
                print("total_pages", total_pages)
                print("start_index", start_index)
                print("end_index", end_index)
                data_list = data_list[start_index:end_index]

                metadata = {
                    "limit": limit,
                    "total_pages": total_pages,
                    "total_records": total_records,
                    "current_page": page_number,
                    "records_per_page": limit,
                    "next_page": f"/users?mode={mode}&column_name={column_name}&order_by={order_by}&page_number={page_number + 1}&limit={limit}" if page_number < total_pages else None,
                    "previous_page": f"/users?mode={mode}&column_name={column_name}&order_by={order_by}&page_number={page_number - 1}&limit={limit}" if page_number > 1 else None
                }

                response = {
                    "metadata": metadata,
                    "data": data_list
                }

                return response
            else:
                return {
                    "metadata": {},
                    "data": []
                }
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    def delete_screening_link(self, screening_id):
        try:
            screening_obj = session.query(ScreeningMaster).filter_by(id = screening_id).first()
            if screening_obj:
                session.delete(screening_obj)
                session.commit()
                return {"status": True, "message": "screening link deleted"}
            else:
                return {"status": False, "message": "screening link not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        
    def get_screening_users(self, screening_code):
        try:
            screening_obj = session.query(ScreeningMaster).filter_by(unique_code = screening_code).first()
            if not screening_obj:
                {"status": False, "message": "screening code not found"}
        
            user_obj = session.query(UserMaster).filter_by(screening_id = screening_obj.id).all()
            return {"status": True, "data": obj_to_list(user_obj)}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def get_placement_details(self, institution_id, column_name, order_by = 'ASC', page_number=1, limit=20):
        try:
            users = session.query(
                UserMaster.id.label('id'),
                UserMaster.student_id,
                UserMaster.first_name,
                UserMaster.last_name,
                UserMaster.phone_number,
                Department.name.label('department_name'),
                func.coalesce(PlacementDetails.status, 'Not Placed').label('status'),
                PlacementDetails.company_name,
                PlacementDetails.company_type,
                PlacementDetails.offer,
                PlacementDetails.offer_type
            )\
            .join(Role, UserMaster.role_id == Role.id)\
            .join(Department, UserMaster.department_id == Department.id)\
            .outerjoin(PlacementDetails, UserMaster.id == PlacementDetails.user_id)\
            .filter(UserMaster.institution_id == institution_id)\
            .filter(Role.name == 'Student')

            if order_by == 'DESC':
                    users = users.order_by(desc(getattr(UserMaster, column_name))).all()
            else:
                users = users.order_by(asc(getattr(UserMaster, column_name))).all()
            

            data_list = [
                {
                    "id": user.id,
                    "student_id": user.student_id,
                    "name": f"{user.first_name} {user.last_name}",
                    "phone_number": user.phone_number,
                    "department_name": user.department_name,
                    "status": user.status,
                    "company_name": user.company_name,
                    "company_type": user.company_type,
                    "offer": user.offer,
                    "offer_type": user.offer_type                    
                }
                for user in users
            ]

            if data_list:
                total_records = len(data_list)
                print("total_records", total_records)
                total_pages = (total_records + limit - 1) // limit
                start_index = (page_number - 1) * limit
                end_index = start_index + limit
                print("limit", limit)
                print("total_pages", total_pages)
                print("start_index", start_index)
                print("end_index", end_index)
                data_list = data_list[start_index:end_index]

                metadata = {
                    "limit": limit,
                    "total_pages": total_pages,
                    "total_records": total_records,
                    "current_page": page_number,
                    "records_per_page": limit,
                    "next_page": f"/placement_tracker/{institution_id}?page_number={page_number + 1}&limit={limit}" if page_number < total_pages else None,
                    "previous_page": f"/placement_tracker/{institution_id}?page_number={page_number - 1}&limit={limit}" if page_number > 1 else None
                }

                response = {
                    "metadata": metadata,
                    "data": data_list
                }

                return response
            else:
                return {
                    "metadata": {},
                    "data": []
                }   

        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}