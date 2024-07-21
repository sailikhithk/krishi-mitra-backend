import requests
import json

from models import (Role, Country, Branch, Department, Course, HardSkill, SoftSkill, 
                    Company, WorkingRole, ReportPoint, InstitutionMaster,
                    InstitutionBranchMapping, BranchCourseMapping, CourseDepartmentMapping

)
from database import session
from sqlalchemy import func
from meta_data import COUNTRIES, ROLES, BRANCHS, DEPARTMENTS, COURSES, BACKEND_SERVER_URL, HARD_SKILLS, SOFT_SKILLS

def create_dummy_roles():
    query_result = (
        session.query(func.count(Role.id)).filter(Role.name.in_(ROLES)).scalar()
    )
    if query_result != len(ROLES):
        for role_name in ROLES:
            existing = session.query(Role).filter_by(name=role_name).first()
            if existing:
                continue

            role = Role(name=role_name)
            session.add(role)
        session.commit()

def create_countries():
    query_result = (
        session.query(func.count(Country.id)).filter(Country.name.in_(COUNTRIES)).scalar()
    )
    if query_result != len(COUNTRIES):
        for country_name in COUNTRIES:
            existing = session.query(Country).filter_by(name=country_name).first()
            if existing:
                continue

            country = Country(name=country_name)
            session.add(country)
        session.commit()

def create_hard_skills():
    query_result = (
        session.query(func.count(HardSkill.id)).filter(HardSkill.name.in_(HARD_SKILLS)).scalar()
    )
    if query_result != len(HARD_SKILLS):
        for name in HARD_SKILLS:
            existing = session.query(HardSkill).filter_by(name=name).first()
            if existing:
                continue
            
            role = HardSkill(name=name)
            session.add(role)
        session.commit()

def create_soft_skills():
    query_result = (
        session.query(func.count(SoftSkill.id)).filter(SoftSkill.name.in_(SOFT_SKILLS)).scalar()
    )
    if query_result != len(SOFT_SKILLS):
        for name in SOFT_SKILLS:
            existing = session.query(SoftSkill).filter_by(name=name).first()
            if existing:
                continue
            
            role = SoftSkill(name=name)
            session.add(role)
        session.commit()

def create_interview_roles():
    json_file_path = 'data/roles_information.json'
    with open(json_file_path, 'r') as json_file:
        ROLES_INFORMATION = json.load(json_file)

    ROLES_INFORMATION_NAMES = [i["role_name"] for i in ROLES_INFORMATION]
    query_result = (
        session.query(func.count(WorkingRole.id)).filter(WorkingRole.name.in_(ROLES_INFORMATION_NAMES)).scalar()
    )
    if query_result != len(ROLES_INFORMATION):
        for role in ROLES_INFORMATION:
            name = role["role_name"]
            responsibilities = role["responsibilities"]
            skills = role["skills"]
            
            existing = session.query(WorkingRole).filter_by(name=name).first()
            if existing:
                continue
            role = WorkingRole(name=name, responsibilities=responsibilities, skills=skills)
            session.add(role)
        session.commit()

# def create_questions():
#     json_file_path = 'data/questions_information.json'
#     with open(json_file_path, 'r') as json_file:
#         QUESTION_INFORMATION = json.load(json_file)

#     for role in QUESTION_INFORMATION:
#         value = QUESTION_INFORMATION[role]
#         role_data = session.query(Question).filter_by(role_name = role).first()
#         if role_data:
#             role_data.value = value
#         else:
#             role = Question(role_name=role, value=value)
#             session.add(role)
#         session.commit()

def create_companies():
    json_file_path = 'data/company_information.json'
    with open(json_file_path, 'r') as json_file:
        COMPANIES_INFORMATION = json.load(json_file)
    query_result = (
        session.query(func.count(Company.id)).filter(Company.name.in_(list(COMPANIES_INFORMATION.keys()))).scalar()
    )
    if query_result != len(COMPANIES_INFORMATION):
        for company_name, company_data in COMPANIES_INFORMATION.items():
            company = Company(
                name=company_name,
                category=company_data.get("category", ""),
                spread_across=company_data.get("spread_across", []),
                working_domain=company_data.get("working_domain", ""),
                about_company=company_data.get("about_company", []),
                latest_news=company_data.get("latest_news", []),
                industry_trends=company_data.get("industry_trends", [])
            )
            session.add(company)
        session.commit()

def create_branches():
    for branch_name in BRANCHS:
        existing = session.query(Branch).filter_by(name=branch_name).first()
        if existing:
            continue

        branch = Branch(name=branch_name)
        session.add(branch)
    session.commit()

def create_departments():
    for department_name in DEPARTMENTS:
        existing = session.query(Department).filter_by(name=department_name).first()
        if existing:
            continue

        department = Department(name=department_name)
        session.add(department)
    session.commit()

def create_courses():
    for course_name in COURSES:
        existing = session.query(Course).filter_by(name=course_name).first()
        if existing:
            continue

        course = Course(name=course_name)
        session.add(course)
    session.commit()

def create_report_points():
    url = f"{BACKEND_SERVER_URL}/user/admin_create_user?mode=teacher"
    json_file_path = 'data/report_points_information.json'
    with open(json_file_path, 'r') as json_file:
        report_points_data = json.load(json_file)    
    
    for point in report_points_data:
        existing = session.query(ReportPoint).filter_by(key = point).first()
        if existing:
            # existing.value = report_points_data[point]
            pass
        else:
            course = ReportPoint(
                key=point,
                value=report_points_data[point]
                )
            session.add(course)
        session.commit()

def create_dummy_institution():
    url = f"{BACKEND_SERVER_URL}/institution/register"
    json_file_path = 'data/institutions_information.json'
    with open(json_file_path, 'r') as json_file:
        institutions_data = json.load(json_file)
    
    for i in institutions_data:
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(i))
        print(response.text)

def create_dummy_students():
    url = f"{BACKEND_SERVER_URL}/user/register"
    json_file_path = 'data/students_information.json'
    with open(json_file_path, 'r') as json_file:
        students_data = json.load(json_file)

    for i in students_data:
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(i))
        print(response.text)

def create_dummy_teachers():
    url = f"{BACKEND_SERVER_URL}/user/admin_create_user?mode=teacher"
    json_file_path = 'data/teachers_information.json'
    with open(json_file_path, 'r') as json_file:
        teachers_data = json.load(json_file)
    
    for i in teachers_data:
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NTA0ODk1NiwianRpIjoiZmUyMThiYzAtYmU0NC00NWRlLThmZmMtODg3MjhiZjA5Nzk4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwiaW5zdGl0dXRpb25fbmFtZSI6IklOViBUZXN0LTEiLCJjb250YWN0X25hbWUiOiJoYXJuYXRoIiwiZW1haWwiOiJoYXJuYXRoLmFAZ21haWwuY29tIiwicGhvbmVfbnVtYmVyIjoiOTcwMTE4NTQ2NyIsImNvdW50cnlfaWQiOjEsImNpdHkiOiJPbmdvbGUiLCJkZXNpZ2FuYXRpb24iOiJTU0UiLCJudW1iZXJfb2Zfc3R1ZGVudHMiOjE1MCwibnVtYmVyX29mX2RlcGFydG1lbnRzIjoxMCwicmVnaXN0cmF0aW9uX251bWJlciI6bnVsbCwiZG9tYWlucyI6IkBnbWFpbC5jb20iLCJwcmVmZXJlbmNlX2RheXMiOiJNb24sIFR1ZSIsInByZWZlcmVuY2VfdGltZSI6IjEwIEFNIHRvIDYgUE0iLCJwYXNzd29yZF9oYXNoIjoiZ0FBQUFBQmxCWVlZZEZzTDZQRzFtMmNXWXYtN1hpTFV2Q2FBbHJjSDRNTmhjQ0VIWEJBaVVkUDl2clYzbGtjb2VrT2xRbmtZNHV5bmhJWkJZT25EZ0todV9FYVp3dkZpQkE9PSIsImlzX2FjdGl2ZSI6dHJ1ZSwiY3JlYXRlZF9kYXRlIjoiMjAyMy0wOS0xNiAxMDowODo0OCIsInVwZGF0ZWRfZGF0ZSI6IjIwMjMtMDktMTYgMTA6NDA6MjQiLCJwYXNzd29yZF9tb2RpZmllZF9kYXRlIjoiMjAyMy0wOS0xNiAxNjoxMDoyNC4xNDUzMjAiLCJsYXN0X2xvZ2luX2RhdGUiOiJOb25lIiwicm9sZV9pZCI6MSwicm9sZV9uYW1lIjoiQWRtaW4ifSwibmJmIjoxNjk1MDQ4OTU2LCJleHAiOjE2OTc2NDA5NTZ9.dLtH6ub4w_IY6DwXbjjIfa1hZlL0tJc1_i6ADGKloxA'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(i))
        print(response.text)

def create_instutation_mapping():
    json_file_path = 'data/institutions_mapping_information.json'
    with open(json_file_path, 'r') as json_file:
        INSTITATION_MAPPING_INFORMATION = json.load(json_file)

    for institution_name in INSTITATION_MAPPING_INFORMATION:
        
        institution_obj = session.query(InstitutionMaster).filter_by(institution_name = institution_name).first()
        if not institution_obj:
            print(f"skiping mapping information for {institution_name} as it is missing create admin account for institution")
            continue
    
        institution_id = institution_obj.id
        print(f"updating information for {institution_name}")
        
        session.query(InstitutionBranchMapping).filter_by(institution_id = institution_id).update({"is_active": 0})
        session.commit()    
        for branch in INSTITATION_MAPPING_INFORMATION[institution_name]:
            
            branch_name = branch["Branch Name"]
            print(f"Branch {branch_name}")
            
            branch_obj = session.query(Branch).filter_by(name = branch_name).first()
            if not branch_obj:
                branch_obj = Branch(name=branch_name)
                session.add(branch_obj)
                session.commit()
                branch_id = branch_obj.id
            else:
                branch_id = branch_obj.id

            branch_mapping_obj = session.query(InstitutionBranchMapping).filter_by(institution_id = institution_id).filter_by(branch_id = branch_id).first()
            if branch_mapping_obj:
               branch_mapping_obj.is_active = True
               session.commit()
            else:
                branch_mapping_obj = InstitutionBranchMapping(
                    institution_id = institution_id,
                    branch_id = branch_id,
                    is_active = True
                )  
                session.add(branch_mapping_obj)
                session.commit()
            
            session.query(BranchCourseMapping).filter_by(branch_id = branch_id).update({"is_active": 0})
            session.commit()    
            for course_name in branch["Courses"]:
                print("course_name", course_name)
                course_obj = session.query(Course).filter_by(name = course_name).first()
                if not course_obj:
                    course_obj = Course(name=course_name)
                    session.add(course_obj)
                    session.commit()
                    course_id = course_obj.id
                else:
                    course_id = course_obj.id
                course_mapping_obj = session.query(BranchCourseMapping).filter_by(course_id = course_id).filter_by(branch_id = branch_id).first()
                if course_mapping_obj:
                    course_mapping_obj.is_active = True
                    session.commit()
                else:
                    course_mapping_obj = BranchCourseMapping(
                        course_id = course_id,
                        branch_id = branch_id,
                        is_active = True
                    )  
                    session.add(course_mapping_obj)
                    session.commit()
                
                departments_information = branch["Departments"][course_name]
                session.query(CourseDepartmentMapping).filter_by(course_id = course_id).update({"is_active": 0})
                session.commit()    
                for department_name in departments_information:
                    print("department_name", department_name)
                    department_obj = session.query(Department).filter_by(name = department_name).first()
                    if not department_obj:
                        department_obj = Department(name=department_name)
                        session.add(department_obj)
                        session.commit()
                        department_id = department_obj.id
                    else:
                        department_id = department_obj.id

                    department_mapping_obj = session.query(CourseDepartmentMapping).filter_by(department_id = department_id).filter_by(course_id = course_id).first()
                    if department_mapping_obj:
                        department_mapping_obj.is_active = True
                        session.commit()
                    else:
                        department_mapping_obj = CourseDepartmentMapping(
                            department_id = department_id,
                            course_id = course_id,
                            is_active = True
                        )
                        session.add(department_mapping_obj)  
                        session.commit()
                        
    session.commit()
