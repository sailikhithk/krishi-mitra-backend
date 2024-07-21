import logging
import traceback
import os

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from jsonschema import validate
from services import UserService
from validation import LOGIN_SCHEMA, USER_RESET_PASSWORD_SCHEMA, USER_REGISTER_SCHEMA, USER_UPDATE_SCHEMA, ALLOWED_EXTENSIONS, USER_UPDATE_PASSWORD_SCHEMA, UPLOAD_USER_ROLE_SCHEMA, STUDENT_CREATED_BY_ADMIN_SCHEMA, TEACHER_CREATED_BY_ADMIN_SCHEMA, USER_REGISTER_INTERVIEW_SCHEMA, SCREENING_USER_REGISTER_SCHEMA, PROCESS_JD_SCHEMA
from access_check import requires_role
from utils import download_sample_file

user_router = Blueprint("user", __name__)
logger = logging.getLogger("user")

user_service_obj = UserService()

@user_router.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        validate(data, USER_REGISTER_SCHEMA)    
        user = user_service_obj.register_user(data)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/report", methods=["GET"])
def report():
    try:
        response = user_service_obj.generate_report()
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/generate_report", methods=["GET"])
def generate_report():
    try:
        interview_id = request.args.get('interview_id')
        response = user_service_obj.generate_report(interview_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/admin_create_user", methods=["POST"])
@jwt_required()
@requires_role("admin")
def create_user():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user.get("id")      
        mode = request.args.get('mode')
        validate(mode, UPLOAD_USER_ROLE_SCHEMA)
        data = request.get_json()

        if mode == "student":
            validate(data, STUDENT_CREATED_BY_ADMIN_SCHEMA)
            data["institution_id"] = institution_id
            response = user_service_obj.admin_create_student(data)
            return jsonify(response)    
        elif mode == "teacher":
            validate(data, TEACHER_CREATED_BY_ADMIN_SCHEMA)
            data["institution_id"] = institution_id
            response = user_service_obj.admin_create_teacher(data)
            return jsonify(response)
        else:
            return jsonify({"status": False, "message": "User not created invalid request"})
                    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        validate(data, LOGIN_SCHEMA)    
        response = user_service_obj.login_user(data)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/logout", methods=["POST"])
def logout():
    try:
        return True
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/reset_password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        validate(data, USER_RESET_PASSWORD_SCHEMA)
        response = user_service_obj.reset_password(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/update_password", methods=["POST"])
@jwt_required()
def update_password():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]      
        data = request.get_json()
        validate(data, USER_UPDATE_PASSWORD_SCHEMA)
        response = user_service_obj.update_password(data, user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/update", methods=["POST"])
def update_user():
    try:
        user_id = request.args.get('user_id')
        data = request.get_json()
        validate(data, USER_UPDATE_SCHEMA)    
        user = user_service_obj.update_user(user_id, data)
        if user:
            response = {"status": True, "message": "User Updated", "data":user} 
        else:
            response = {"status": False, "message": "User not updated"} 
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/list", methods=["GET"])
@jwt_required()
def list_users():
    try:
        current_user = get_jwt_identity()
        current_role = current_user["role_name"]
        if current_role in ('Teacher', 'Student'):
            user_id = current_user["id"]
            institution_id = current_user["institution_id"]
        else:
            institution_id = current_user["id"]

        mode = request.args.get('mode', 'Student')
        column_name = request.args.get('column_name', "created_date")
        order_by = request.args.get('order_by', 'DESC')
        page_number = int(request.args.get('page_number', 1))
        records_per_page = int(request.args.get('limit', 20))       
        branch_name = request.args.get('branch_name')
        department_name  = request.args.get('department_name')
        users = user_service_obj.list_users(institution_id, mode, column_name, order_by, page_number, records_per_page, branch_name, department_name)
        return jsonify(users)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/user_by_department_list", methods=["GET"])
@jwt_required()
def user_by_department_list():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]      
        department_id = request.args.get('department_id', 0)
        users = user_service_obj.user_by_department_list(institution_id, department_id)
        return jsonify(users)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/delete", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def delete_user():
    try:
        user_id = request.args.get('user_id')
        status = user_service_obj.delete_user(user_id)
        if status:
            response = {"status": True, "message": "User Deleted"} 
        else:
            response = {"status": False, "message": "User not deleted"} 

        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/<int:user_id>/activate", methods=["GET"])
@jwt_required()
@requires_role("admin")
def activate_user(user_id):
    try:
        return jsonify(user_service_obj.activate_user(user_id))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/<int:user_id>/deactivate", methods=["GET"])
@jwt_required()
@requires_role("admin")
def deactivate_user(user_id):
    try:
        return jsonify(user_service_obj.deactivate_user(user_id))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/upload", methods=["POST"])
@jwt_required()
@requires_role("admin")
def upload_users():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        
        data = request.get_json()
        mode = data["mode"]        
        validate(mode, UPLOAD_USER_ROLE_SCHEMA)
        response = user_service_obj.upload_users(data, institution_id, mode)  
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route('/download', methods=['GET'])
def download_users():
    try:
        sample_data = request.args.get('sample_data', False)
        mode = request.args.get('mode', 'student')
        data_dir = os.path.join(os.path.dirname(__file__), 'data/sample_upload_files')
        data_dir = data_dir.replace("/routes", "")
        # file_name = user_service_obj.download_create_users_file(mode, sample_data)
        file_name = download_sample_file(mode, sample_data)
        print("Filename", file_name)
        print("data_dir", data_dir)
        file_path = os.path.join(data_dir, file_name)
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404
    

@user_router.route("/statistics", methods=["GET"])
@jwt_required()
@requires_role("student,teacher,screening")
def user_statistics():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        user_role = str(current_user["role_name"]).lower()
        if user_role == 'teacher':
            response = user_service_obj.teacher_statistics(user_id)
        elif user_role == 'student':
            response = user_service_obj.student_statistics(user_id)
        elif user_role == 'screening':
            response = user_service_obj.screening_statistics(user_id)
        else:
            response = user_service_obj.student_statistics(user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user_router.route("/register_interview", methods=["POST"])
@jwt_required()
def register_interview():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        role_name = current_user["role_name"]
        data = request.get_json()
        validate(data, USER_REGISTER_INTERVIEW_SCHEMA)
        data["user_id"] = user_id
        response = user_service_obj.register_interview(data, role_name)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/submit_answer", methods=["POST"])
@jwt_required()
def submit_answer():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        
        data = request.get_json()
        data["user_id"] = user_id
        response = user_service_obj.submit_answer(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/list_interviews", methods=["GET"])
def list_interviews():
    try:
        user_id = request.args.get('user_id', None)
        interview_filter = request.args.get('interview_filter', "")
        page_number = int(request.args.get('page_number', 1))
        records_per_page = int(request.args.get('limit', 20))       
        
        status = request.args.get('status', "completed,report_inprogress,report_generated")
        status = status.split(",")
        response = user_service_obj.interview_list(user_id, status, interview_filter, page_number, records_per_page)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@user_router.route("/update_interview", methods=["POST"])
@jwt_required()
def update_interview():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        data = request.get_json()
        data["user_id"] = user_id
        response = user_service_obj.update_interview(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



@user_router.route("/prioritize_interview", methods=["POST"])
@jwt_required()
def prioritize_interview():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        interview_id = request.args.get('status')
        response = user_service_obj.prioritize_interview(user_id, interview_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@user_router.route("/deprioritize_interview", methods=["POST"])
@jwt_required()
def deprioritize_interview():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        interview_id = request.args.get('status')
        response = user_service_obj.deprioritize_interview(user_id, interview_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@user_router.route("/generate_report_test", methods=["GET"])
def generate_report_test():
    try:
        interview_id =1
        response = user_service_obj.generate_report(interview_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/register_screening_user", methods=["POST"])
def register_screening_user():
    try:
        data = request.get_json()
        validate(data, SCREENING_USER_REGISTER_SCHEMA)
        response = user_service_obj.register_screening_user(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/is_interview_allowed", methods=["GET"])
@jwt_required()
def is_interview_allowed():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        response = user_service_obj.is_interview_allowed(user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user_router.route("/process_jd", methods=["POST"])
@jwt_required()
@requires_role("student")
def process_jd():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        data = request.get_json()
        validate(data, PROCESS_JD_SCHEMA)
        response = user_service_obj.process_jd(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
