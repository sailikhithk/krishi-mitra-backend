import traceback
import base64
import os
import copy
import random
import json
import pandas as pd
from datetime import datetime
from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader

from flask_jwt_extended import create_access_token

from models import (UserMaster, InstitutionMaster, Role, Branch, Department, Course, InterviewMaster, 
                    Question, ReportPoint, Company, WorkingRole, TrainingCourse, QuestionBankMaster, 
                    Assignment, ScreeningMaster)

from collection_models import (HardSkillImprovementSuggestions, SoftSkillImprovementSuggestions, 
                               EmotionsSuggestions, HardSkillQuestions, SoftSkillQuestions,
                               HrQuestions, SoftSkillCustomQuestions, HardSkillCustomQuestions, 
                               CompanyRoleCustomQuestions, CulturalSkillCustomQuestions)



from meta_data import UPLOAD_USER_FILE_STUDENT_HEADERS, UPLOAD_USER_FILE_TEACHER_HEADERS, BACKEND_SERVER_URL, UI_SERVER_URL, INTERVIEW_IMPROVEMENTS 
from utils import encrypt, decrypt, obj_to_dict, obj_to_list
from database import session
from email_utils import send_email
from ai_generator import generate_company_based_questions, generate_skill_questions, extract_required_techical_skills, generate_jd_skill_questions, generate_cultural_skill_questions
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import desc, asc, func

from google_module import GoogleDriveManager
from dotenv import load_dotenv
load_dotenv()



class UserService:
    def __init__(self):
        pass

    def get_user_by_id(self, id):
        return session.query(UserMaster).filter_by(id=id).first()

    def get_institution_by_id(self, id):
        return session.query(InstitutionMaster).filter_by(id=id).first()
    
    def get_user_by_email(self, email):
        return session.query(UserMaster).filter_by(email = email).first()
    
    def login_user(self, data):
        try:
            email = data["email"]
            email = str(email).strip().lower()
            password = data["password"]
            user = self.get_user_by_email(email)
            if not user:
                return {"message": "Invalid username or password", "status": False}

            if not user.is_active:
                return {"message": "User deactivated contact admin", "status": False}

            hashpwd = user.password_hash
            db_password = decrypt(hashpwd)
            
            if db_password == password:
                user_data = obj_to_dict(user)
                role_id = user.role_id
                role = session.query(Role).filter_by(id = role_id).first()
                branch = session.query(Branch).filter_by(id = user.branch_id).first()
                course = session.query(Course).filter_by(id = user.course_id).first()
                institution = session.query(InstitutionMaster).filter_by(id = user.institution_id).first()
                user_data["role_name"] = role.name
                user_data["branch_name"] = branch.name
                user_data["course_name"] = course.name
                user_data["institution_name"] = institution.institution_name
                access_token = create_access_token(identity=user_data)
                return {"message": "", "status": True, "access_token": access_token, "data": user_data}
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
            email = str(email).strip().lower()
            hashed_password = encrypt(password)
            
            user = self.get_user_by_email(email)
            if not user:
                return {"message": "Invalid creds", "status": False}        
            
            user.password_hash = hashed_password
            user.password_modified_date = datetime.now()
            
            session.commit()
            return {"message": "Password updated, relogin again", "status": True}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}

    def update_password(self, data, user_id):
        try:
            password = data["new_password"]
            hashed_password = encrypt(password)
            
            user = self.get_user_by_id(user_id)
            if not user:
                return {"message": "Invalid creds", "status": False}        
            user.password_hash = hashed_password
            user.password_modified_date = datetime.now()
            session.commit()
            return {"message": "Password updated, relogin again", "status": True}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def register_screening_user(self, data):
        try:
            unique_code = data.get("unique_code")

            if not unique_code:
                return {"status": False, "message": "invalid registration request"}
        
            screening_master_obj = session.query(ScreeningMaster).filter_by(unique_code = unique_code).first()
            
            if not screening_master_obj:
                return {"status": False, "message": "invalid registration request"}
            
            if not screening_master_obj.is_active:
                return {"status": False, "message": "registration time completed contact adman"}
                       
            expiry_date = screening_master_obj.expiry_date
            activation_date = screening_master_obj.activation_date
            institution_id = screening_master_obj.created_by
            screening_id = screening_master_obj.id
            max_capacity = screening_master_obj.max_capacity
            current_date = datetime.now()

            institution_obj = session.query(InstitutionMaster).filter_by(id = institution_id).first()
            institution_name = institution_obj.institution_name

            if activation_date <= current_date <= expiry_date:
                pass
            else:
                return {"status": False, "message": "invalid registration request"}
            
            from .institution_services import InstitutionService
            institution_service = InstitutionService()

            screening_users_response = institution_service.get_screening_users(unique_code)
            # if not screening_users_response["status"]:
            #     return screening_users_response
            
            current_capacity = screening_users_response.get("data", [])
            
            if len(current_capacity) >= max_capacity:
                return {"status": False, "message": "Screening capacity is full"}
                        
            data["password_hash"] = encrypt(data["password"])
            original_password = data["password"]
            data.pop("password")
            data["initial_password_reset"] = True
            data["screening_id"] = screening_id
            data["institution_id"] = institution_id
            email = data["email"]
            email = str(email).strip().lower()
            existing_user = self.get_user_by_email(email)
            if existing_user:    
                return {"status": False, "message": "User with same email exists already"}
                     
            role = session.query(Role).filter_by(name = "Screening").first()
            data["role_id"] = role.id
        
            
            branch_id = institution_service.create_branch(data.get("branch_name"))
            data["branch_id"] = branch_id
            institution_service.create_institution_branch_mapping(institution_id, branch_id, institution_name,data.get("branch_name"))
            
            course_id = institution_service.create_course(data.get("course_name"))
            data["course_id"] = course_id
            institution_service.create_branch_course_mapping(branch_id, data.get("course_id"), data.get("branch_name"),data.get("course_name"))
            
            department_id = institution_service.create_department(data.get("department_name"))
            data["department_id"] = department_id
            institution_service.create_course_department_mapping(course_id, department_id, data.get("course_name"), data.get("department_name"))
            
            
            data.pop("branch_name", None)
            data.pop("course_name", None)
            data.pop("department_name", None)
            data.pop("unique_code", None)
            
            user = UserMaster(**data)
            session.add(user)
            session.commit()
            user_dic = obj_to_dict(user)
            
            if user_dic:
                email_values = {
                    "user_name": user.email,
                    "institution_name": institution_obj.institution_name,
                    "password": original_password,
                    "login_url": UI_SERVER_URL    
                }
                send_email("institution_register.html",user.email, "User Registered", email_values)
                response = {"status": True, "message": "User Created", "data":user_dic}
            else:
                response = {"status": False, "message": "User not created"}
            return response
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}

    def is_interview_allowed(self, user_id):
        try:
            user = session.query(UserMaster).filter_by(id = user_id).first()
            if not user:
                return {"status": True, "allowed": False, "message": "user not found"}

            screening_id = user.screening_id
            if not screening_id:
                return {"status": True, "allowed": False, "message": "user not found"}
            
            screening_obj = session.query(ScreeningMaster).filter_by(id = screening_id).first()
            if not screening_obj:
                return {"status": True, "allowed": False, "message": "user not found"}
            
            max_interviews = int(os.environ.get("MAX_SCREENING_INTERVIEWS", 5))

            user_interview_count = session.query(InterviewMaster).filter_by(user_id = user_id).count()

            if  user_interview_count < max_interviews:
                return  {"status": True, "allowed": True}
            
            return  {"status": True, "allowed": False, "message": "max interview limit reached"}    
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "allowed": False}

    def register_user(self, data):
        try:
            data["password_hash"] = encrypt(data["password"])
            original_password = data["password"]
            data.pop("password")
            data["initial_password_reset"] = True
            
            email = data["email"]
            email = str(email).strip().lower()
            data["email"] = email
            existing_user = self.get_user_by_email(email)
            print("existing_user", existing_user)
            if existing_user:    
                return {"status": False, "message": "User with same email exists"}
                     
            if "role_id" not in data:
                role = session.query(Role).filter_by(name = "Student").first()
                data["role_id"] = role.id
            
            # if "course" not in data:
            #     course = session.query(Course).filter_by(name = data['course']).first()
            #     if course is not None:
            #         data["course_id"] = course.id
            #     else:
            #         course = session.query(Course).filter_by(name = "UG").first()
            #         data["course_id"] = course.id
            # data.pop("course", None)
                
            if "course_id" not in data:
                course = session.query(Course).filter_by(name = "UG").first()
                data["course_id"] = course.id
            
            user = UserMaster(**data)
            session.add(user)
            session.commit()
            user_dic = obj_to_dict(user)
            
            institution = self.get_institution_by_id(user.institution_id)
            if user_dic:
                email_values = {
                    "user_name": user.email,
                    "institution_name": institution.institution_name,
                    "password": original_password,
                    "login_url": UI_SERVER_URL    
                }
                send_email("institution_register.html",user.email, "User Registered", email_values)
                response = {"status": True, "message": "User Created", "data":user_dic}
            else:
                response = {"status": False, "message": "User not created"}
            return response
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}

    def admin_create_student(self, data):
        try:
            role_id = self.convert_name_to_id(session, Role, 'name', "Student")
            data["role_id"] = role_id        
            data["password_hash"] = encrypt(data["password"])
            original_password = data["password"]
            data.pop("password")
            data["initial_password_reset"] = False
            email = data['email']
            email = str(email).strip().lower()
            data['email'] = email
            user = self.get_user_by_email(email)

            if user:
                print(f"User(Student) with email {email} already exists")
                return {"status": False, "message": "Student with same email exists, new student not created"}
            
            user = UserMaster(**data)
            session.add(user)
            session.commit()
            user_dic = obj_to_dict(user)
            institution = self.get_institution_by_id(user.institution_id)
            if user_dic:
                email_values = {
                    "user_name": user.email,
                    "institution_name": institution.institution_name,
                    "password": original_password,
                    "login_url": UI_SERVER_URL    
                }
                send_email("institution_register.html",user.email, "User Registered", email_values)
            return {"status": True, "message": "Student Created", "new_user_id":user.id}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def admin_create_teacher(self, data):
        try:
            role_id = self.convert_name_to_id(session, Role, 'name', "Teacher")
            data["role_id"] = role_id
            data["password_hash"] = encrypt(data["password"])
            original_password = data["password"]
            data.pop("password")
            data["initial_password_reset"] = False
            email = data['email']
            email = str(email).strip().lower()
            data['email'] = email
            user = self.get_user_by_email(email)
            if user:
                print(f"User(Teacher) with email {email} already exists")
                return {"status": False, "message": "Teacher with same email exists, new teacher not created"}
            
            user = UserMaster(**data)
            session.add(user)
            session.commit()
            user_dic = obj_to_dict(user)
            institution = self.get_institution_by_id(user.institution_id)
            if user_dic:
                email_values = {
                    "user_name": user.email,
                    "institution_name": institution.institution_name,
                    "password": original_password,
                    "login_url": UI_SERVER_URL    
                }
                send_email("institution_register.html",user.email, "User Registered", email_values)
            return {"status": True, "message": "Teacher Created", "user_id":user.id}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def update_user(self, user_id, update_data):
        try:
            user = session.query(UserMaster).get(user_id)
            
            if user:
                for key, value in update_data.items():
                    setattr(user, key, value)  
                session.commit()
            user_dic = obj_to_dict(user)
            return user_dic
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
       
    def list_users(self, institution_id, mode, column_name, order_by = 'ASC', page_number=1, limit=20, branch_name = None, department_name = None):
        try:
            print("branch_name", branch_name)
            print("department_name", branch_name)
            print("mode", mode)
            print("institution_id", institution_id)

            if mode == "Student":
                users = session.query( 
                                    UserMaster.first_name,
                                    UserMaster.last_name,
                                    func.count(InterviewMaster.id).label("total_number_of_interviews_attempted"),
                                    UserMaster.id,
                                    UserMaster.phone_number,
                                    UserMaster.address,
                                    UserMaster.email,
                                    UserMaster.created_date,
                                    UserMaster.is_active,
                                    Branch.name.label("branch_name"), 
                                    Department.name.label("department_name"),
                                    InstitutionMaster.institution_name.label("institution_name"), 
                                    Course.name.label("course_name")) \
                    .join(Role, UserMaster.role_id == Role.id) \
                    .join(Branch, UserMaster.branch_id == Branch.id) \
                    .join(Department, UserMaster.department_id == Department.id) \
                    .join(InstitutionMaster, UserMaster.institution_id == InstitutionMaster.id) \
                    .join(Course, UserMaster.course_id == Course.id) \
                    .outerjoin(InterviewMaster, UserMaster.id == InterviewMaster.user_id)\
                    .filter(Role.name == mode)\
                    .filter(InstitutionMaster.id == institution_id)
                    
                if branch_name:
                    users = users.filter(Branch.name == branch_name)

                if department_name:
                    users = users.filter(Department.name == department_name)
                                
                
                users = users.group_by(UserMaster.id, Branch.name, Department.name, InstitutionMaster.institution_name, Course.name, UserMaster.first_name, UserMaster.last_name, UserMaster.phone_number, UserMaster.address, UserMaster.email, UserMaster.created_date, UserMaster.is_active)
                
                if order_by == 'DESC':
                    users = users.order_by(desc(getattr(UserMaster, column_name))).all()
                else:
                    users = users.order_by(asc(getattr(UserMaster, column_name))).all()
                print("users", users)
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
                        "id": student_id,
                        "name": f"{user.first_name} {user.last_name}",
                        "phone_number": user.phone_number,
                        "address": user.address,
                        "email": user.email,
                        "branch_name": user.branch_name,
                        "department_name": user.department_name,
                        "institution_name": user.institution_name,
                        "no_of_interviews": len(scorelist),
                        "total_number_of_interviews_attempted": user.total_number_of_interviews_attempted,
                        "avg_score": round(average,2),
                        "course_name": user.course_name,
                        "created_date": str(user.created_date),
                        "is_active": user.is_active
                    })
            elif mode == "Teacher":
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
                                    Branch.name.label("branch_name"), 
                                    Department.name.label("department_name"),
                                    InstitutionMaster.institution_name.label("institution_name"), 
                                    Course.name.label("course_name")) \
                    .join(Role, UserMaster.role_id == Role.id) \
                    .join(Branch, UserMaster.branch_id == Branch.id) \
                    .join(Department, UserMaster.department_id == Department.id) \
                    .join(InstitutionMaster, UserMaster.institution_id == InstitutionMaster.id) \
                    .join(Course, UserMaster.course_id == Course.id)\
                    .filter(Role.name == mode)\
                    .filter(InstitutionMaster.id == institution_id) 
                
                if branch_name:
                    users = users.filter(Branch.name == branch_name)

                if department_name:
                    users = users.filter(Department.name == department_name)
                
                if order_by == 'DESC':
                    users = users.order_by(desc(getattr(UserMaster, column_name))).all()
                else:
                    users = users.order_by(asc(getattr(UserMaster, column_name))).all()
                
                data_list = [
                {
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}",
                    "phone_number": user.phone_number,
                    "address": user.address,
                    "email": user.email,
                    "branch_name": user.branch_name,
                    "department_name": user.department_name,
                    "institution_name": user.institution_name,
                    "avg_score": 50,
                    "course_name": user.course_name,
                    "created_date": str(user.created_date),
                    "is_active": user.is_active,
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
            return {"error": str(e), "status": False}
    
    def user_by_department_list(self, institution_id, department_id):
        try:
            role_obj = session.query(Role).filter_by(name = "Student").first()
            student_role_id = role_obj.id
            
            if department_id:
                users_obj = session.query(UserMaster).filter_by(department_id = department_id).filter_by(institution_id = institution_id).filter_by(role_id = student_role_id)
            else:
                users_obj = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(role_id = student_role_id)
            
            users_obj = users_obj.order_by(desc(getattr(UserMaster, "created_date"))).all()
            
            result_data = []
            for user in users_obj:
                result_data.append({
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}"
                })            
            return {"status": True, "data": result_data}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}

    def delete_user(self, user_id):
        try:
            user = session.query(UserMaster).get(user_id)
            
            if user:
                session.delete(user)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
        
    def activate_user(self, user_id):
        try:
            user = session.query(UserMaster).get(user_id)
            
            if user:
                user.is_active = True
                session.commit()
                return {"status": True, "message": "User Activated"} 
            else:
                return {"status": False, "message": "User not Activated"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def deactivate_user(self, user_id):
        try:
            user = session.query(UserMaster).get(user_id)
            
            if user:
                user.is_active = False
                session.commit()
                return {"status": True, "message": "User Activated"} 
            else:
                return {"status": False, "message": "User not Activated"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def management(self, institution_id):
        try:
            students_obj = session.query(UserMaster).join(Role).filter(UserMaster.institution_id == institution_id).filter(Role.name == 'Student').all()
            teachers_obj = session.query(UserMaster).join(Role).filter(UserMaster.institution_id == institution_id).filter(Role.name == 'Teacher').all()

            students = obj_to_list(students_obj)
            teachers = obj_to_list(teachers_obj)
            students_df = pd.DataFrame(students)
            teachers_df = pd.DataFrame(teachers)
            unique_student_departments = students_df["department_id"].nunique()
            unique_teacher_departments = teachers_df["department_id"].nunique()
            
            unique_student_branchs = students_df["branch_id"].nunique()
            unique_teacher_branchs = teachers_df["branch_id"].nunique()
            
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
            return {"error": str(e), "status": False}

    def convert_name_to_id(self, session, model_class, name_col, name_value):
        entity = session.query(model_class).filter_by(name=name_value).first()
        if entity:
            return entity.id
        return None
    
    def upload_users(self, data, institution_id, mode): 
        try:
            print("mode", mode)
            file_data = base64.b64decode(data['base64'])
            file_data_name = f'uploaded_file_{institution_id}_{mode}.xlsx'
                
            with open(file_data_name, 'wb') as video_file:
                video_file.write(file_data)
            
            data_df = pd.read_excel(file_data_name, engine='openpyxl')
            df_columns = data_df.columns.tolist()
            df_new_columns = {k:str(k).lower().strip().replace(" ", "_") for k in df_columns}
            data_df.rename(columns=df_new_columns, inplace=True)
            df_columns = data_df.columns.tolist()
            
            print("Columns in uploaded file", df_columns)
            print("Columns in teacher validation", UPLOAD_USER_FILE_TEACHER_HEADERS)
            print("Columns in student validation", UPLOAD_USER_FILE_STUDENT_HEADERS)
                
            if mode == 'student':
                # uploaded student file
                for column in df_columns:
                    if column not in UPLOAD_USER_FILE_STUDENT_HEADERS:
                        print("Missing", column)
                        return {"status": False, "message": "Invalid File"}    
                for index, row in data_df.iterrows():
                    email = row['email']
                    email = str(email).strip().lower()
            
                    user = self.get_user_by_email(email)
                    if user:
                        print(f"User(Student) with email {email} already exists")
                        continue
                    
                    branch_id = self.convert_name_to_id(session, Branch, 'name', row['branch'])
                    department_id = self.convert_name_to_id(session, Department, 'name', row['department'])
                    course_id = self.convert_name_to_id(session, Course, 'name', row['course'])
                    role_id = self.convert_name_to_id(session, Role, 'name', "Student")
                    
                    password = str(row["password"])
                    hashed_password = encrypt(password)

                    user = UserMaster(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        phone_number=row['phone_number'],
                        email=str(email).strip().lower(),
                        branch_id=branch_id,
                        department_id=department_id,
                        institution_id=institution_id,
                        programme = "",
                        address = row.get('address', ""),
                        role_id=role_id,
                        course_id=course_id,
                        password_hash = hashed_password,
                        student_id = row.get('student_id', "")
                    )
                    session.add(user)

                    user_dic = obj_to_dict(user)
                    institution = self.get_institution_by_id(user.institution_id)
                    if user_dic:
                        email_values = {
                            "user_name": user.email,
                            "institution_name": institution.institution_name,
                            "password": password,
                            "login_url": UI_SERVER_URL    
                        }
                        send_email("institution_register.html",user.email, "User Registered", email_values)
            
                session.commit()
                
                return {"status": True, "message": "User uploaded"}
            elif mode == 'teacher':
                # uploaded teacher file                    
                for column in df_columns:
                    if column not in UPLOAD_USER_FILE_TEACHER_HEADERS:
                        print("Missing", column)
                        return {"status": False, "message": "Invalid File"}    
            
                for index, row in data_df.iterrows():
                    email = row['email']
                    user = self.get_user_by_email(email)
                    if user:
                        print(f"User(Teacher) with email {email} already exists")
                        continue
                    
                    branch_id = self.convert_name_to_id(session, Branch, 'name', row['branch'])
                    department_id = self.convert_name_to_id(session, Department, 'name', row['department'])
                    role_id = self.convert_name_to_id(session, Role, 'name', 'Teacher')

                    password = str(row["password"])
                    hashed_password = encrypt(password)

                    user = UserMaster(
                        first_name=row['first_name'],
                        phone_number=row['phone_number'],
                        email=str(email).strip().lower(),
                        branch_id=branch_id,
                        department_id=department_id,
                        institution_id=institution_id,
                        role_id=role_id,
                        address = row.get('address', ""),
                        password_hash = hashed_password
                    )
                    session.add(user)
                    
                    user_dic = obj_to_dict(user)
                    institution = self.get_institution_by_id(user.institution_id)
                    if user_dic:
                        email_values = {
                            "user_name": user.email,
                            "institution_name": institution.institution_name,
                            "password": password,
                            "login_url": UI_SERVER_URL    
                        }
                        send_email("institution_register.html",user.email, "User Registered", email_values)
            
                session.commit()
                
                return {"status": True, "message": "Teachers uploaded"}
            else:
                return {"status": False, "message": "Invalid File"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
        
    # def download_create_users_file(self, mode, sample_data = False): 
    #     try:
    #         if str(mode).lower() == 'student':
    #             if sample_data:
    #                 file_name = "students_upload_with_sample_data.xlsx"
    #             else:
    #                 file_name = "students_upload.xlsx"
    #         else:
    #             if sample_data:
    #                 file_name = "teachers_upload_with_sample_data.xlsx"
    #             else:
    #                 file_name = "teachers_upload.xlsx"
        
    #         return file_name
        
        
    #     except Exception as e:
    #         session.rollback()
    #         traceback.print_exc()
    #         return ""
    
    def average_percentage_change(self, numbers):
        if numbers is None:
            return (0, "No Change")
        percentage_changes = []
        
        for i in range(1, len(numbers)):
            previous = numbers[i - 1]
            current = numbers[i]
            if previous == 0:
                percentage_change = current * 100
            else:    
                percentage_change = ((current - previous) / previous) * 100
            percentage_changes.append(percentage_change)
        
        if len(percentage_changes) == 0:
            return (0, "No Change")
        
        average_change = sum(percentage_changes) / len(percentage_changes)
        
        # Determine if the change is positive or negative
        direction = "Positive" if average_change > 0 else "Negative"
        
        return (average_change, direction)

    def get_hard_skill_suggestions(self, skill_name, no_of_suggestions = 2):
        try:
            result = HardSkillImprovementSuggestions.objects(name=skill_name).first()
            suggestions = []
            if result:
                suggestions = result.suggestions
            return random.sample(suggestions, no_of_suggestions)
        except Exception as e:
            return []
        
    def get_soft_skill_suggestions(self, skill_name, no_of_suggestions = 2):
        try:
            result = SoftSkillImprovementSuggestions.objects(name=skill_name).first()
            suggestions = []
            if result:
                suggestions = result.suggestions
            return random.sample(suggestions, no_of_suggestions)
        except Exception as e:
            return []
        
    def get_emotion_suggestions(self, emotion_name, no_of_suggestions=1):
        try:
            result = EmotionsSuggestions.objects(name=emotion_name).first()
            suggestions = []
            if result:
                suggestions = result.suggestions
            return random.sample(suggestions, no_of_suggestions)
        except Exception as e:
            return []
        
    def get_skill_questions(self, skill_mode, skill_name, level, count = 0, no_of_questions = 5, role_name = None):
        try:
            tag = ""
            if skill_mode == 'hard_skill':
                if role_name == "Screening":
                    result = HardSkillCustomQuestions.objects(name=skill_name).first()
                    if not result:
                        result = HardSkillQuestions.objects(name=skill_name).first()
                
                else:
                    result = HardSkillQuestions.objects(name=skill_name).first()
                
                
                if not result:
                    print(f"Questions not available for skill {skill_mode} so generating it")
                    generate_skill_questions(skill_name, 'hard_skill')
                    result = HardSkillQuestions.objects(name=skill_name).first() 
                
                tag = "technical"
                
            elif skill_mode == 'soft_skill':
                if role_name == "Screening":
                    result = SoftSkillCustomQuestions.objects(name=skill_name).first()
                    if not result:
                        result = SoftSkillQuestions.objects(name=skill_name).first()
                else:
                    result = SoftSkillQuestions.objects(name=skill_name).first()
                
                if not result:
                    print(f"Questions not available for skill {skill_mode} so generating it")
                    generate_skill_questions(skill_name, 'soft_skill')
                    result = SoftSkillQuestions.objects(name=skill_name).first()
                
                tag = "behavioral"
            
            elif skill_mode == 'hr_skill':
                result = HrQuestions.objects(name='hr').first()
                if not result:
                    print(f"Questions not available for skill {skill_mode} so generating it")
                    generate_skill_questions('hr', 'hr_skill')
                    result = SoftSkillQuestions.objects(name=skill_name).first()
                tag = "hr"
            
            elif skill_mode == 'cultural_skill':
                result = CulturalSkillCustomQuestions.objects(name=skill_name).first()
                
                if not result:
                    print(f"Questions not available for skill {skill_mode} so generating it")
                    generate_skill_questions(skill_name, 'soft_skill')
                    result = CulturalSkillCustomQuestions.objects(name=skill_name).first()
                tag = "cultural"
            
            else:
                return []
            questions = []
            
            if result: 
                if level.lower() == 'beginner':
                    questions = result.beginner
                elif level.lower() == 'intermediate':
                    questions = result.intermediate
                elif level.lower()  in ['expert', 'export']:
                    questions = result.export
                    if not questions:
                        questions = result.expert

            
            print("questions", questions)
            final_list = []
            if questions:
                selected_indices = random.sample(range(2, len(questions) - 2), no_of_questions)
            
                for i in selected_indices:
                    count = count + 1
                    final_list.append({
                            "id": count,
                            "tag": tag,
                            "question": questions[i],
                            "duration": 60,
                            "category": skill_mode,
                            "sub_category": skill_name
                        }
                    )    
            
            print("final_list", final_list)
            return final_list
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            return []

    def student_statistics(self, user_id):
        try:
            response = {
                "cards": [],
                "graphs": []
            }
            

            interviews = session.query(InterviewMaster).filter_by(user_id = user_id)
            interview_objs = interviews.all()
            user_obj = session.query(UserMaster).filter_by(id = user_id).first()
            print('user obj================================', user_obj)
            
            
            jd_interviews_obj = interviews.filter(InterviewMaster.status == 'report_generated').filter(InterviewMaster.interview_type == 'jd_interview').all()
            jd_interviews_count = len(jd_interviews_obj)
            
            cultural_interviews_obj = interviews.filter(InterviewMaster.status == 'report_generated').filter(InterviewMaster.interview_type == 'cultural_interview').all()
            cultural_interviews_count = len(cultural_interviews_obj)
            
            card_1 = {
                "name": "Number of JD Interviews Conducted",
                "value": jd_interviews_count
            }
            
            card_2 = {
                "name": "Number of cultural Interviews Conducted",
                "value": cultural_interviews_count
            }
            
            response["cards"] = [card_1, card_2]
            
            graph_1_data = []
            count = 1
            for interview_obj in interview_objs:
                result_json = interview_obj.result_json
                if not result_json:
                    continue

                interview_Score_Trend = result_json.get("Interview Score Trend")
                if not interview_Score_Trend:
                    continue

                interview_Score_Trend["name"] = str(count)
                graph_1_data.append(interview_Score_Trend)
                count = count + 1

            graph_1 = {
                "name": "My Interview Score Trend",
                "data": graph_1_data
            }
            
            
            graph_2_data = []
            for jd_interview_obj in jd_interviews_obj:
                report_json = jd_interview_obj.report_json
                
                if not report_json:
                    continue
                
                interview_position = report_json.get("interview_position")
                interview_company = report_json.get("interview_company")
                interview_graph_data = report_json.get("graph_data")
                graph_2_data.append({
                    "company_name": interview_company,
                    "role": interview_position,
                    "data": interview_graph_data
                })
            
            graph_3_data = []
            for cultural_interview_obj in cultural_interviews_obj:
                report_json = cultural_interview_obj.report_json
                
                if not report_json:
                    continue
                
                interview_position = report_json.get("interview_position")
                interview_company = report_json.get("interview_company")
                interview_graph_data = report_json.get("graph_data")
                graph_3_data.append({
                    "company_name": interview_company,
                    "role": interview_position,
                    "data": interview_graph_data
                })
                            
            graph_2 = {
                "name": "JD Interview skill overview",
                "data": graph_2_data
            }
            
            graph_3 = {
                "name": "Cultural Interview skill overview",
                "data": graph_3_data
            }
            
            response["graphs"] = [graph_1, graph_2, graph_3]            
            
            interview_improvement_suggestions = []
            uncertified_hard_skills = user_obj.uncertified_hard_skills
            uncertified_soft_skills = user_obj.uncertified_soft_skills
            negative_emotions = user_obj.negative_emotions
            if uncertified_hard_skills:
                uncertified_hard_skills_list = uncertified_hard_skills.split(",")
                selected_skill = random.sample(uncertified_hard_skills_list, 2)
                interview_improvement_suggestions.extend(self.get_hard_skill_suggestions(selected_skill))

            if uncertified_soft_skills:
                uncertified_soft_skills_list = uncertified_soft_skills.split(",")
                selected_skill = random.sample(uncertified_soft_skills_list, 2)
                interview_improvement_suggestions.extend(self.get_soft_skill_suggestions(selected_skill))

            if negative_emotions:
                negative_emotions_list = negative_emotions.split(",")
                selected_emotion = random.sample(negative_emotions_list, 1)
                interview_improvement_suggestions.extend(self.get_emotion_suggestions(selected_emotion))

            if len(interview_improvement_suggestions) < 5:
                interview_improvement_suggestions.extend(random.sample(INTERVIEW_IMPROVEMENTS,5-len(interview_improvement_suggestions)))

            hard_skill_avg_score_list = user_obj.hard_skill_avg_score
            if not hard_skill_avg_score_list:
                hard_skill_avg_score_list = "0"
            hard_skill_avg_score_list = list(map(float, hard_skill_avg_score_list.split(',')))
            
            soft_skill_avg_score_list = user_obj.soft_skill_avg_score
            if not soft_skill_avg_score_list:
                soft_skill_avg_score_list = "0"
            soft_skill_avg_score_list = list(map(float, soft_skill_avg_score_list.split(',')))
            
            response["skill_trends"] = {
                "hard_skill": 0,
                "soft_skill": 0
            }         
            skill_trends_hard_skill, direction = self.average_percentage_change(hard_skill_avg_score_list)
            if not skill_trends_hard_skill:
                skill_trends_hard_skill = 0

            skill_trends_soft_skill, direction = self.average_percentage_change(soft_skill_avg_score_list)  
            if not skill_trends_soft_skill:
                skill_trends_soft_skill = 0

            response["skill_trends"]["hard_skill"] = round(float(skill_trends_hard_skill),2)
            response["skill_trends"]["soft_skill"] = round(float(skill_trends_soft_skill),2)  
            response["suggestions"] = interview_improvement_suggestions
            return {"status": True, "data": response}

        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def teacher_statistics(self, user_id, institution_id, branch_id):
        try:
            response = {
                "cards": [],
                "graphs": []
            }

            # Graphs 
            # 1. Number of assignments Vs Month
            # 2. Student Vs No.of assignments schedules Vs No.of assignments schedules attempted Vs 


            role_obj = session.query(Role).filter_by(name = "Student").first()
            student_role_id = role_obj.id
            role_obj = session.query(Role).filter_by(name = "Teacher").first()
            teacher_role_id = role_obj.id

            active_students_count = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(is_active = True).filter_by(role_id = student_role_id).filter_by(branch_id = branch_id).count()
            
            inactive_students_count = session.query(UserMaster).filter_by(institution_id = institution_id).filter_by(is_active = False).filter_by(role_id = student_role_id).filter_by(branch_id = branch_id).count()
            
            no_of_courses = session.query(TrainingCourse).filter_by(created_by = user_id).count()

            no_of_questionbanks = session.query(QuestionBankMaster).filter_by(created_by = user_id).count()

            no_of_assingments = session.query(Assignment).filter_by(created_by = user_id).count()

            card_1 = {
                "name": "Number of Students",
                "value": active_students_count + inactive_students_count,
                "sub_values": {
                    "active": active_students_count,
                    "in_active": inactive_students_count
                }                
            }

            card_2 = {
                "name": "Number of Courses",
                "value": no_of_courses
            }
            
            card_3 = {
                "name": "Number of Question Banks",
                "value": no_of_questionbanks
            }
            
            card_4 = {
                "name": "Number of Assignments",
                "value": no_of_assingments
            }
            
            response["cards"] = [card_1, card_2, card_3, card_4]
            
            institution_obj = session.query(InstitutionMaster).filter_by(id = institution_id).first()
            if not institution_obj:
                return {"status": False, "message": "Wrong institution"}    
            
            return {"status": True, "data": response}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        

    def screening_statistics(self, user_id):
        try:
            max_interviews = int(os.environ.get("MAX_SCREENING_INTERVIEWS", 5))
            user_interview_count = session.query(InterviewMaster).filter_by(user_id = user_id).count()

            card_1 = {
                "name": "Number of Interviews Allocated",
                "value": max_interviews
            }
            
            card_2 = {
                "name": "Number of Interviews Conducted",
                "value": user_interview_count
            }

            response = {
                "cards": [],
                "graphs": []
            }
            
            response["cards"] = [card_1, card_2] 
            return {"status": True, "data": response}
                        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        

    def register_skill_interview(self, data, role_name):
        try:
            level = data.get("level", "Beginner")
            
            specifications = data.get("specifications", {})
                
            hard_skill_names = specifications.get("hard_skill", [])
            soft_skill_names = specifications.get("soft_skill", [])

            questions = []

            len_hard_skill = len(hard_skill_names)
            len_soft_skill = len(soft_skill_names)
            
            len_total_skills = len_hard_skill + len_soft_skill

            if len_total_skills == 1:
                no_of_questions = 10
            else:
                no_of_questions = 5
            
            if hard_skill_names and soft_skill_names:
                            
                for hard_skill_name in hard_skill_names:
                    questions.extend(self.get_skill_questions('hard_skill', hard_skill_name, level, len(questions), no_of_questions, role_name))                                     

                for soft_skill_name in soft_skill_names:
                    questions.extend(self.get_skill_questions('soft_skill', soft_skill_name, level, len(questions), no_of_questions, role_name))

            elif hard_skill_names:
                for hard_skill_name in hard_skill_names:
                    questions.extend(self.get_skill_questions('hard_skill', hard_skill_name, level, len(questions), no_of_questions, role_name))
            elif soft_skill_names:
                for soft_skill_name in soft_skill_names:
                    questions.extend(self.get_skill_questions('soft_skill', soft_skill_name, level, len(questions), no_of_questions, role_name))
            
            questions.extend(self.get_skill_questions('hr_skill', 'hr', level, len(questions)))
            return questions
        except Exception as e:
            traceback.print_exc()
            return questions
            
    def register_company_role_interview(self, data, role_name):
        try:
            level = data.get("level", "Beginner")
            specifications = data.get("specifications", {})
            
            company_role_name = specifications.get("role", "Software Developer")
            company_name = specifications.get("company", "Google")
            
            questions = []

            questions.extend(generate_company_based_questions(level, company_role_name, company_name, role_name))
            
            questions.extend(self.get_skill_questions('hr_skill', 'hr', level, len(questions)))
            
            return questions
        
        except Exception as e:
            traceback.print_exc()
            return questions

    def register_jd_interview(self, data):
        try:
            specifications = data.get("specifications", {})
            jd_skills = specifications.get("jd_skill", [])
            questions = []
            if jd_skills:
                for jd_skill in jd_skills:
                    jd_skill = jd_skill.strip().lower()
                    questions.extend(generate_jd_skill_questions(jd_skill, len(questions)))
                return questions
            else:
                return []           
        except Exception as e:
            traceback.print_exc()
            return []

    def register_cultural_interview(self, data):
        try:
            specifications = data.get("specifications", {})
            cultural_skills = specifications.get("cultural_skill", [])
            questions = []
            if cultural_skills:
                for cultural_skill in cultural_skills:
                    cultural_skill = cultural_skill.strip().lower()
                    questions.extend(generate_cultural_skill_questions(cultural_skill, len(questions)))
                return questions
            else:
                return []           
        except Exception as e:
            traceback.print_exc()
            return []
        
    def register_interview(self, data, role_name):
        try:
            interview_type = str(data.get("interview_type", "")).strip().lower()
            specifications = data.get("specifications", {})
            no_sec = 60
            
            
            if "level" in specifications:
                if str(specifications["level"]).lower() == 'low':
                    data["level"] = "Beginner"    
                elif str(specifications["level"]).lower() == 'high':
                    data["level"] = "Expert"
                    no_sec = 300
                elif str(specifications["level"]).lower() == 'mid':
                    data["level"] = "Intermediate"
                    no_sec = 180
                else:
                    data["level"] = "Beginner"
            else:
                data["level"] = "Beginner"
            
            data["status"] = "Not Started"
            data["interview_type"] = interview_type
            
            
            if interview_type == "":
                return {"status": False, "message": "Interview type is required"}
            elif interview_type == "skill_interview": 
                questions = self.register_skill_interview(data, role_name)
            elif interview_type == "company_role_interview":
                questions = self.register_company_role_interview(data, role_name)
            elif interview_type == "jd_interview":
                questions = self.register_jd_interview(data)
            elif interview_type == "cultural_interview":
                questions = self.register_cultural_interview(data)
            else:
                return {"status": False, "message": "Invalid interview type"}
            
            interview = InterviewMaster(**data)
            session.add(interview)
            session.commit()
            interview_dic = obj_to_dict(interview)
            print("interview_dic", interview_dic)
            
            return {"status": True, "questions": questions,"interview_id": interview.id}
                    
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def submit_answer(self, data):
        try:
            user_id = str(data["user_id"])
            interview_id = str(data["interview_id"])
            interview_status = str(data["status"])
            interview_status = str(interview_status).lower().strip().replace(" ", "_")
            question = str(data["question"])
            question_id = data["question_id"]
            tag = data["tag"]
            category = data["category"]
            sub_category = data["sub_category"]

            
            video_data = base64.b64decode(data['video'])
            video_file_name = f'{user_id}_{interview_id}_{int(question_id)-1}_video.mp4'  # as we have a issue with video processing of last question this us the hard fix for that
            
            interview = session.query(InterviewMaster).filter_by(id = interview_id).first()
            if not interview:
                return {"status": False, "message": "Interview not exist"}
            
            path_json = interview.path_json

            with open(video_file_name, 'wb') as video_file:
                video_file.write(video_data)
            

            google_drive_object =  GoogleDriveManager()
            
            # checking folder for that user based on user_id
            print("user_id", user_id)
            user_based_folder = google_drive_object.folder_exists_by_name(user_id)
            user_based_folder_id = user_based_folder.get('id')
            print("user folder id", user_based_folder_id)
            if not user_based_folder_id:
                user_based_folder_id = google_drive_object.create_folder(user_id)

            interview_based_folder = google_drive_object.folder_exists_by_name(interview_id, user_based_folder_id)
            interview_based_folder_id = interview_based_folder.get('id') 
            print("interview folder id", interview_based_folder_id)
            if not interview_based_folder_id:
                interview_based_folder_id = google_drive_object.create_folder(interview_id, user_based_folder_id)
            

            file_details = google_drive_object.create_file(video_file_name, interview_based_folder_id, video_file_name)
            print("file_details", file_details)
            file_details_id = file_details["id"]
            
            temp_data = {
                "question":question,
                "answer_source_path":file_details_id,
                "question_id": question_id,
                "tag": tag,
                "category": category,
                "sub_category": sub_category
            }
            # print(f"Existing path_json from database to interview id {interview_id}", path_json)
            # print("type path_json", type(path_json))
            # print("Current submitted answer code:", temp_data)
            if path_json:
                temp_data_2 = copy.deepcopy(path_json)
                # as we have a issue with video processing of last question this us the hard fix for that 
                temp_data_2_last_index_data = temp_data_2[-1]
                temp_data_2_last_index_data["answer_source_path"] = temp_data["answer_source_path"]
                temp_data_2[-1] = temp_data_2_last_index_data
                temp_data_2.append(temp_data)
            else:
                temp_data_2 = [temp_data]
                
            # print("After update Final path_json is ", temp_data_2)
            interview.status = interview_status
            interview.path_json = temp_data_2
            session.commit()
            os.remove(video_file_name)
            return {"status":True, "file_details": file_details}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def generate_report(self, interview_id):
        readiness_score_list = []
        presentation_and_grooming_list = []
        interview_obj = session.query(InterviewMaster).filter_by(id = interview_id).first()
        if not interview_obj:
            return {"status": False, "message": "invalid Interview"}
        
        COMPANY_NAME = os.environ.get("COMPANY_NAME")
        COMPANY_NUMBER = os.environ.get("COMPANY_NUMBER")
        COMPANY_EMAIL = os.environ.get("COMPANY_EMAIL")
        COMPANY_WEBSITE = os.environ.get("COMPANY_WEBSITE")
        DEFAULT_TEACHER_NAME = os.environ.get("DEFAULT_TEACHER_NAME", "Manu R")
        DEFAULT_TEACHER_NUMBER = os.environ.get("DEFAULT_TEACHER_NUMBER", "+91 8328057448")

        report_points = session.query(ReportPoint).all()
        report_point_dic = {}
        for report_point in report_points:
            report_point_dic[report_point.key] = report_point.value

        interview_specifications = interview_obj.specifications
            
        user_id = interview_obj.user_id
        interview_type = interview_obj.interview_type
        user_obj = session.query(UserMaster).filter_by(id = user_id).first()
        branch_id = user_obj.branch_id
        
        role_obj = session.query(Role).filter_by(name = "Teacher").first()
        
        # teacher_role_id = role_obj.id
        # teacher_obj = session.query(UserMaster).filter_by(branch_id = branch_id).filter_by(role_id = teacher_role_id).first()
        # teacher_name = DEFAULT_TEACHER_NAME
        # teacher_number = DEFAULT_TEACHER_NUMBER
        # if teacher_obj:
        #     teacher_name = f"{teacher_obj.first_name} {teacher_obj.last_name}".strip()
        #     teacher_number = teacher_obj.phone_number

        teacher_name = ""
        teacher_number = ""
        
        # institution_id = user_obj.institution_id
        # institution_obj = session.query(InstitutionMaster).filter_by(id = institution_id).first()
        
        user_name = f"{user_obj.first_name} {user_obj.last_name}"
        ds_result_json = interview_obj.result_json

        soft_skill_avg_score = ds_result_json.get("soft_skill_avg_score")
        hard_skill_avg_score = ds_result_json.get("hard_skill_avg_score")
                
        behavioral_presentation_and_grooming = {}
        interview_score_by_category = {}
        
        behavioral_presentation_and_grooming["title"] = "Behavioral Presentation and Grooming"
        behavioral_presentation_and_grooming["data"] = []
        
        interview_score_by_category["title"] = "Interview Score By Category"
        interview_score_by_category["data"] = []

        ds_behavioral_presentation_and_grooming = ds_result_json.get("Behavioral Presentation and Grooming", {})
        for key,value in ds_behavioral_presentation_and_grooming.items():
            # "Eye contact rating": "9/10"
            secured_marks = int(value.split('/')[0])
            total_marks = int(value.split('/')[-1])
            notes = f"{user_name} ,{report_point_dic.get(key, {}).get(str(secured_marks), '')}"
            presentation_and_grooming_list.append(secured_marks)
            behavioral_presentation_and_grooming["data"].append({
                "title": key,
                "secured_marks": secured_marks,
                "total_marks": total_marks,
                "notes": notes 
            })

        
        ds_interview_score_by_category = ds_result_json.get("Interview Score By Category", {})
        
        # print("ds_interview_score_by_category", ds_interview_score_by_category)
        for key,cat in ds_interview_score_by_category.items():
            main_title = key
            title =  cat.get("main_segment", "")
            secured_marks = int(cat.get(title, "0/10").split('/')[0])           
            total_marks = int(cat.get(title, "0/10").split('/')[-1])
            # readiness_score_list.append(secured_marks)
            notes = f"{user_name} ,{report_point_dic.get(title, {}).get(str(secured_marks), '')}"
            interview_questions = cat.get("interview_questions", [])
            
            cat.pop('main_segment', None)
            cat.pop(title, None)
            cat.pop("interview_questions", None)
            sub_segements = []
            
            for key2, val2 in cat.items():
                score = val2["Score"]
                sub_secured_marks = int(score.split('/')[0])
                sub_total_marks = int(score.split('/')[-1])
                sub_notes = val2.get("Justification", "")
                if not sub_notes:
                    sub_notes = f"{user_name} ,{report_point_dic.get(key2, {}).get(str(secured_marks), '')}"
                
                sub_segements.append({
                    "title": key2,
                    "secured_marks": sub_secured_marks,
                    "total_marks": sub_total_marks,
                    "notes": sub_notes 
                })
            
            interview_score_by_category["data"].append(
                {
                    "main_title": main_title,
                    "title": title,
                    "secured_marks": secured_marks,
                    "total_marks": total_marks,
                    "notes": notes,
                    "sub_segements": sub_segements,
                    "interview_questions": interview_questions
                }
            )
        
        about_company = []
        company_latest_news = []
        company_industry_trends=[]
                    
        if "readiness_score" in ds_result_json:
            readiness_score = ds_result_json.get("readiness_score")
        else:
            readiness_score =  round(sum(readiness_score_list)/len(readiness_score_list),2),
            
        report_json = {
            "interview_position": interview_specifications.get("role"),
            "interview_company": interview_specifications.get("company"),
            "readiness_score": readiness_score,
            "presentation_and_grooming_score": round(sum(presentation_and_grooming_list)/len(presentation_and_grooming_list), 2),
            "source_company": COMPANY_NAME,
            "source_company_number": COMPANY_NUMBER,
            "source_company_email": COMPANY_EMAIL,
            "source_company_websites": COMPANY_WEBSITE,
            "user_name": user_name,
            "teacher_name": teacher_name, 
            "teacher_number": teacher_number,
            "behavioral_presentation_and_grooming": behavioral_presentation_and_grooming,
            "interview_score_by_category": interview_score_by_category,  
            "where_you_stand": {
            "percentage": "75%",
            "content": 50,
            "content_highlight": 3
            },
            
        }        
        
        # Harnath need to inform 
        # report_type = ds_result_json.get("report_type")
        # report_json["report_type"] = report_type
        if interview_type == "skill_interview":
            
            # skills report from DS 
            qualified_hard_skills = ds_result_json.get("qualified_hard_skills", [])
            qualified_soft_skills = ds_result_json.get("qualified_soft_skills", [])
            unqualified_hard_skills = ds_result_json.get("unqualified_hard_skills", [])
            unqualified_soft_skills = ds_result_json.get("unqualified_soft_skills", [])
            # midqualified_hard_skills = ds_result_json.get("midqualified_hard_skills", [])
            # midqualified_soft_skills = ds_result_json.get("midqualified_soft_skills", [])
            
                    
            # hard skills block from user master
            certified_hard_skills = user_obj.certified_hard_skills
            if certified_hard_skills:
                if certified_hard_skills == '[]':
                    certified_hard_skills = ""
                certified_hard_skills = certified_hard_skills.split(',')
            else:
                certified_hard_skills = []

            uncertified_hard_skills = user_obj.uncertified_hard_skills
            if uncertified_hard_skills:
                if uncertified_hard_skills == '[]':
                    uncertified_hard_skills = ""
                uncertified_hard_skills = uncertified_hard_skills.split(',')
            else:
                uncertified_hard_skills= []

            # intermediate_hard_skills = user_obj.intermediate_hard_skills
            # if intermediate_hard_skills:
            #     intermediate_hard_skills = intermediate_hard_skills.split(',')
            # else:
            #     intermediate_hard_skills= []

            # soft skills block from user master
            certified_soft_skills = user_obj.certified_soft_skills
            if certified_soft_skills:
                if certified_soft_skills == '[]':
                    certified_soft_skills = ""
                certified_soft_skills = certified_soft_skills.split(',')
            else:
                certified_soft_skills = []

            uncertified_soft_skills = user_obj.uncertified_soft_skills
            if uncertified_soft_skills:
                if uncertified_soft_skills == '[]':
                    uncertified_soft_skills = ""
                uncertified_soft_skills = uncertified_soft_skills.split(',')
            else:
                uncertified_soft_skills= []

            # intermediate_soft_skills = user_obj.intermediate_soft_skills
            # if intermediate_soft_skills:
            #     intermediate_soft_skills = intermediate_soft_skills.split(',')
            # else:
            #     intermediate_soft_skills= []

            # hard skills block from user master
            certified_hard_skills = user_obj.certified_hard_skills
            if certified_hard_skills:
                if certified_hard_skills == '[]':
                    certified_hard_skills = ""
                certified_hard_skills = certified_hard_skills.split(',')
            else:
                certified_hard_skills = []

            uncertified_hard_skills = user_obj.uncertified_hard_skills
            if uncertified_hard_skills:
                if uncertified_hard_skills == '[]':
                    uncertified_hard_skills = ""
                uncertified_hard_skills = uncertified_hard_skills.split(',')
            else:
                uncertified_hard_skills= []

            print("Before Update")
            print("certified_hard_skills", certified_hard_skills)
            print("qualified_hard_skills", qualified_hard_skills)
            print("certified_soft_skills", certified_soft_skills)
            print("qualified_soft_skills", qualified_soft_skills)
                        
            # updating certified_hard_skills and certified_soft_skills in db
            for i in qualified_hard_skills:
                if i not in certified_hard_skills:
                    certified_hard_skills.append(i)
                if i in uncertified_hard_skills:
                    uncertified_hard_skills.remove(i)

            for i in unqualified_hard_skills:
                if i in certified_hard_skills:
                    continue
                if i not in uncertified_hard_skills:
                    uncertified_hard_skills.append(i)
        
            for i in qualified_soft_skills:
                if i not in certified_soft_skills:
                    certified_soft_skills.append(i)
                if i in uncertified_soft_skills:
                    uncertified_soft_skills.remove(i)

            for i in unqualified_soft_skills:
                if i in certified_soft_skills:
                    continue
                if i not in uncertified_soft_skills:
                    uncertified_soft_skills.append(i)

            certified_hard_skills.extend(qualified_hard_skills)
            new_qualified_hard_skills = list(set(certified_hard_skills))

            certified_soft_skills.extend(qualified_soft_skills)
            new_qualified_soft_skills = list(set(certified_soft_skills))

            user_obj.certified_hard_skills = ','.join(new_qualified_hard_skills)
            user_obj.certified_soft_skills = ','.join(new_qualified_soft_skills)
            
            hard_skill_avg_score_list = user_obj.hard_skill_avg_score
            soft_skill_avg_score_list = user_obj.soft_skill_avg_score
            if hard_skill_avg_score_list:
                hard_skill_avg_score_list = str(hard_skill_avg_score_list).strip().split(",")
            else:
                hard_skill_avg_score_list =  []
            
            if soft_skill_avg_score_list:
                soft_skill_avg_score_list = str(soft_skill_avg_score_list).strip().split(",")
            else:
                soft_skill_avg_score_list =  []

            if hard_skill_avg_score is not None:
                hard_skill_avg_score_list.append(hard_skill_avg_score)
                
            if soft_skill_avg_score is not None:
                soft_skill_avg_score_list.append(soft_skill_avg_score)
                
            user_obj.hard_skill_avg_score = ','.join(list(map(str, hard_skill_avg_score_list)))
            user_obj.soft_skill_avg_score = ','.join(list(map(str, soft_skill_avg_score_list)))
                
            print("After")
            print("hard_skill_avg_score_list", hard_skill_avg_score_list)
            print("soft_skill_avg_score_list", soft_skill_avg_score_list)
            
            session.commit()
            # print("user_obj.id", user_obj.id)
            # print("user_obj.hard_skill_avg_score", user_obj.hard_skill_avg_score)
            # print("user_obj.soft_skill_avg_score", user_obj.soft_skill_avg_score)

            report_json["hard_and_soft_skill_dic"] = ds_result_json.get("hard_and_soft_skill_dic", {})
            report_json["skill_based_suggestions"] = ds_result_json.get("skill_based_suggestions")

        elif interview_type == "company_role_interview":
            interview_position = interview_specifications.get("role")
            interview_company = interview_specifications.get("company")
        
            
            role_specific_skills =[]
            if interview_position:
                working_role_obj = session.query(WorkingRole).filter_by(name = interview_position).first()
                role_specific_skills = working_role_obj.skills

            company_obj = session.query(Company).filter_by(name = interview_company).first()
            about_company = company_obj.about_company
            company_latest_news = company_obj.latest_news
            company_industry_trends=company_obj.industry_trends
        
            report_json["about_company"] = about_company
            report_json["lastest_company_news"] = company_latest_news
            report_json["role_specific_skills"] = role_specific_skills
            report_json["industry_trends"] = company_industry_trends
                   
        elif interview_type in ["jd_interview", "cultural_interview"]:
            
            graph_data = []
            skill_details_dic = ds_result_json.get("hard_and_soft_skill_dic", {})

            interview_type_skill_details_dic = skill_details_dic.get(interview_type.lower().strip().replace("interview", "skill"), {})
            
            for key, value in interview_type_skill_details_dic.items():
                graph_data.append(
                    {
                    "skill_name": key, 
                   "scored": value * 2,
                   "total": 10,
                    })
            report_json["graph_data"] = graph_data

        report_json["interview_type"] = interview_type
        interview_obj.report_json = report_json
        interview_obj.status = 'report_generated'
        session.commit()
        
        email_values = {
                    "user_name": f"{user_obj.first_name} {user_obj.last_name}",
                    "interview_id": interview_obj.id,
                    "login_url": UI_SERVER_URL    
                }
        send_email("report_notification.html",user_obj.email, "Report Generated", email_values)
                
        return {"status": True, "data": report_json}
            
    def interview_list(self, user_id, status_list = ["completed", "report_inprogress", "report_generated"], interview_filter = "", page_number = 1, records_per_page = 10):
        query = session.query(InterviewMaster)
        
        if user_id:
            query = query.filter_by(user_id = user_id)
        
        if status_list:
            query = query.filter(InterviewMaster.status.in_(status_list))
        
        if interview_filter:
            interview_filter = interview_filter.strip().lower().split(",")
            query = query.filter(InterviewMaster.interview_type.in_(interview_filter))
        
        
        interviews_obj = query.order_by(desc(getattr(InterviewMaster, "created_date"))).all()    
        print("interviews_obj", interviews_obj)
        interviews_list = obj_to_list(interviews_obj)
        
        if interviews_list:
            total_interviews = len(interviews_list)
            print("total_interviews", total_interviews)
            total_pages = (total_interviews + records_per_page - 1) // records_per_page
            start_index = (page_number - 1) * records_per_page
            end_index = start_index + records_per_page
            print("records_per_page", records_per_page)
            print("total_pages", total_pages)
            print("start_index", start_index)
            print("end_index", end_index)
            interviews_list = interviews_list[start_index:end_index]

            metadata = {
                        "limit": records_per_page,
                        "total_pages": total_pages,
                        "total_records": total_interviews,
                        "current_page": page_number,
                        "records_per_page": records_per_page,
                        "next_page": f"/list_interviews?interview_filter={interview_filter}&limit={records_per_page}&page_number={page_number + 1}&status={','.join(status_list)}" if page_number < total_pages else None,
                        "previous_page": f"/list_interviews?interview_filter={interview_filter}&limit={records_per_page}&page_number={page_number - 1}&status={','.join(status_list)}" if page_number > 1 else None
                    }
            response = {
                        "metadata": metadata,
                        "data": interviews_list,
                        "satus": True
                    }
                        
            return response
        else:
            return {"data": [], "satus": True, "metadata": {}}

    
    def update_interview(self, interview_id, data):
        try:
            interview = session.query(InterviewMaster).filter_by(id = interview_id).first()
        
            if interview:
                for key, value in data.items():
                    setattr(interview, key, value)  
                session.commit()
            interview_dic = obj_to_dict(interview)
            return interview_dic
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
       
    def prioritize_interview(self, user_id, interview_id):
        interview = session.query(InterviewMaster).filter_by(id = interview_id).first()
        interview.prioritize = True
        session.commit() 
        return {"status": True, "message": "Interview prioritize"}
    
    def deprioritize_interview(self, user_id, interview_id):
        interview = session.query(InterviewMaster).filter_by(id = interview_id).first()
        interview.prioritize = False
        session.commit() 
        return {"status": True, "message": "Interview prioritize"}
    
    def get_list_course(self, user_id):
        try:
            courses = session.query(Course).filter_by(created_by = user_id).all()
            return {"status": True, "courses": obj_to_list(courses)}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Courses not found"}
        
    def process_jd(self, data):
        try:
            mode = data.get("mode")
            company_name = data.get("company_name")
            company_role = data.get("company_role")
            interview_type = data.get("interview_type")
            
            jd_file = data.get("file")
            jd_file_name = data.get("file_name")
            jd_text = data.get("text")
            
            if mode == "file":
                # need to process base 64 to text 
                decoded_bytes = base64.b64decode(jd_file)
                
                if jd_file_name.endswith(".docx"):
                    file_stream = BytesIO(decoded_bytes)
                    document = Document(file_stream)
                    jd_text = "\n".join([paragraph.text for paragraph in document.paragraphs])
                
                elif jd_file_name.endswith(".pdf"):
                    file_stream = BytesIO(decoded_bytes)
                    reader = PdfReader(file_stream)
                    jd_text = "\n".join([page.extract_text() for page in reader.pages])
                
                else:
                    try:
                        jd_text = decoded_bytes.decode("utf-8")
                    except Exception as e:
                        jd_text = decoded_bytes.decode("iso-8859-1")

            if company_name:
                jd_text = jd_text + f"Company name: {company_name}"
            
            if company_role:
                jd_text = jd_text + f"Company role: {company_role}"
            
            
            required_skills = extract_required_techical_skills(jd_text, interview_type)
            if required_skills:
                required_skills = required_skills[0].split(",")
            else:
                required_skills = []
            
            required_skills = list(map(str.strip, required_skills))
            return {"status": True, "required_skills": required_skills}
        
        except Exception as e:
            traceback.print_exc()
            return {"error": str(e), "status": False}