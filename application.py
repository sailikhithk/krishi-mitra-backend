# main.py
import os
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import timedelta


# Registering the blueprints after initializing the application
from routes.user import user_router
from routes.institution import institution_router
from routes.course import course_router
from routes.assignment import assignment_router
from routes.question_bank import question_bank_router
from routes.admin import admin_router

from access_check import requires_role

# from routes.case_master import case_master as case_master_router
from flask_jwt_extended import decode_token, JWTManager, jwt_required, get_jwt_identity

from database import Base, engine, initialize_mongodb

application = Flask(__name__)

application.config["JWT_SECRET_KEY"] = "your-secret-key"
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
application.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
jwt = JWTManager(application)

# Apply CORS to application
CORS(application, resources={r"*": {"origins": "*"}})


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Mango DB connection
initialize_mongodb()

# Registering the blueprints
application.register_blueprint(user_router, url_prefix="/user")
application.register_blueprint(institution_router, url_prefix="/institution")
application.register_blueprint(course_router, url_prefix="/course")
application.register_blueprint(assignment_router, url_prefix="/assignment")
application.register_blueprint(question_bank_router, url_prefix="/question_bank")
application.register_blueprint(admin_router, url_prefix="/admin")

@application.before_request
def before_request():
    print()
    print("Request Received:")
    print("URL:", request.url)
    print("Method:", request.method)
    # print("Headers:", request.headers)
    print("Query Params:", request.args)
    
    if request.method == "POST":
        if request.content_type.startswith('application/json'):
            body = request.get_json()
            if 'video' in body:
                print("There is a video component in the response so not printing the body")
            else:
                print("Body (JSON):", request.get_json())
        elif request.content_type.startswith('multipart/form-data'):
            print("Form Data:")
            for key, value in request.form.items():
                if key != "file":
                    print(f"{key}: {value}")    
    else:
        print("Body: No request body")
    
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({"message": "Access token is missing", "status": False}), 401

@application.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST")
    
    print()
    print("Response Sent:")
    print("Status Code:", response.status_code)
    print("Content Type:", response.content_type)
    
    if response.content_type == "application/json":
        print("Data:", response.get_json())
    elif response.content_type.startswith("image/") or response.content_type.startswith("application/"):
        print("File Response: Not Printing Binary Data")
    else:
        print("Data:", response.get_data(as_text=True))    
    return response



@application.cli.command('insert_dummy_data')
def insert_dummy_data():
    with application.app_context():
        from create_db import (
            create_dummy_roles,
            create_countries,
            create_branches,
            create_departments,
            create_courses,
            create_dummy_institution,
            create_dummy_teachers,
            create_dummy_students,
            # create_hard_skills,
            # create_soft_skills,
            create_interview_roles,
            create_companies,
            # create_questions,
            create_report_points,
            create_instutation_mapping
        )
    # print("Inserting Roles")
    # create_dummy_roles()
    # print("Inserting Country")
    # create_countries()
    # print("Inserting Branch")
    # create_branches()
    # print("Inserting Courses")
    # create_courses()
    # print("Inserting Departments")
    # create_departments()
    
    # print("Inserting Institution")
    # create_dummy_institution()
    print("Inserting Teachers")
    create_dummy_teachers()
    print("Inserting Students")
    create_dummy_students()
    # print("Inserting Hard Skills")
    # create_hard_skills()
    # print("Inserting Soft Skills")
    # create_soft_skills()
    # print("Inserting Interview Roles")
    # create_interview_roles()
    # print("Inserting companies")
    # create_companies()
    # print("Inserting Report Points")
    create_report_points()
    
    # print("Inserting Questions")
    # create_questions()
    
    # print("Inserting Instutation Mapping")
    # create_instutation_mapping()
    print("Dummy data insert completed")
 
@application.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({"status": "Flask server is working fine"})

@application.route('/insert_dummy_data', methods=['GET'])
def insert_dummy_data_api():
    from create_db import (
        create_dummy_roles,
        create_countries,
        create_branches,
        create_departments,
        create_courses,
        create_dummy_institution,
        create_dummy_teachers,
        create_dummy_students,
        # create_hard_skills,
        # create_soft_skills,
        create_interview_roles,
        create_companies,
        # create_questions,
        create_report_points,
        create_instutation_mapping
    )
    print("Inserting Roles")
    create_dummy_roles()
    print("Inserting Country")
    create_countries()
    # print("Inserting Branch")
    # create_branches()
    # print("Inserting Courses")
    # create_courses()
    # print("Inserting Departments")
    # create_departments()
    # print("Inserting Institution")
    # create_dummy_institution()
    print("Inserting Teachers")
    create_dummy_teachers()
    print("Inserting Students")
    create_dummy_students()
    # print("Inserting Hard Skills")
    # create_hard_skills()
    # print("Inserting Soft Skills")
    # create_soft_skills()
    # print("Inserting Interview Roles")
    # create_interview_roles()
    # print("Inserting companiespanies")
    # create_companies()
    # print("Inserting Questions")
    # create_questions()
    print("Inserting Report points")
    create_report_points()
    # print("Inserting Instutation Mapping")
    # create_instutation_mapping()
    print("Dummy data insert completed")
    return jsonify({"status": "Sample data inserted"})

@application.route('/', methods=['GET'])
def root_api():
    return jsonify({"status": "Flask server is working fine"})

if __name__ == "__main__":
    # SQL Models
    from models.branch import Branch
    from models.country import Country
    from models.department import Department
    from models.institution_master import InstitutionMaster
    from models.role import Role
    from models.user_master import UserMaster
    from models.course import Course
    from models.company import Company
    from models.hard_skill import HardSkill
    from models.soft_skill import SoftSkill
    from models.working_role import WorkingRole
    from models.interview_master import InterviewMaster
    from models.report_point import ReportPoint
    from models.question import Question  
    from models.institution_branch_mapping import InstitutionBranchMapping
    from models.branch_course_mapping import BranchCourseMapping
    from models.course_department_mapping import  CourseDepartmentMapping
    from models.assignment import Assignment
    from models.question_bank import QuestionBankMaster
    from models.configuration_history import ConfigurationHistory
    from models.assignment_user_mapping import AssignmentUserMapping
    from models.institution_company_mapping import InstitutionCompanyMapping
    from models.institution_hard_skill_mapping import InstitutionHardSkillMapping
    from models.institution_soft_skill_mapping import InstitutionSoftSkillMapping
    from models.training_course import TrainingCourse
    from models.training_course_user_mapping import TrainingCourseUserMapping
    from models.screening_master import ScreeningMaster
    from models.assignment_results import AssignmentResults
    from models.entity_master import EntityMaster
    from models.entity_mapping import EntityMapping
  
    # NoSQL Models
    from collection_models.hard_skill_improvement_suggestions import HardSkillImprovementSuggestions
    from collection_models.soft_skill_improvement_suggestions import SoftSkillImprovementSuggestions
    from collection_models.emotions_suggestions import EmotionsSuggestions
    from collection_models.hard_skill_questions import HardSkillQuestions
    from collection_models.hr_questions import HrQuestions
    from collection_models.role_questions import CompanyRoleQuestions
    from collection_models.soft_skill_questions import SoftSkillQuestions
    from collection_models.role_custom_questions import CompanyRoleCustomQuestions
    from collection_models.hard_skill_custom_questions import HardSkillCustomQuestions
    from collection_models.soft_skill_custom_questions import SoftSkillCustomQuestions
    from collection_models.course_content import CourseContent
    from collection_models.cultural_skill_questions import CulturalSkillCustomQuestions
    
    
    Base.metadata.create_all(engine)
    application.run(host='0.0.0.0', port=5000)
