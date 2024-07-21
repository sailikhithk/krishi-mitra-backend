import logging
import traceback
import threading
import os
import json
import base64

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from jsonschema import validate
from services import InstitutionService
from validation import INSTITUTION_REGISTER_SCHEMA, INSTITUTION_UPDATE_SCHEMA, LOGIN_SCHEMA, RESET_PASSWORD_SCHEMA, INSTITUTION_UPDATE_PASSWORD_SCHEMA, ANALYSIS_MODE_SCHEMA, INSTITUTION_CONFIGURATION_SCHEMA, GENERATE_SCREENING_LINK_SCHEMA
from access_check import requires_role
from utils import download_sample_file
institution_router = Blueprint("institution", __name__)
logger = logging.getLogger("institution")

institution_service_obj = InstitutionService()


@institution_router.route("/register", methods=["POST"])
def register_institution():
    try:
        data = request.get_json()
        validate(data, INSTITUTION_REGISTER_SCHEMA)    
        return jsonify(institution_service_obj.register_institution(data))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/login", methods=["POST"])
def login_institution():
    try:
        data = request.get_json()
        validate(data, LOGIN_SCHEMA)
        response = institution_service_obj.login_institution(data)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/country_list", methods=["GET"])
def country_list():
    try:
        response = institution_service_obj.country_list()
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/branch_list", methods=["GET"])
def branch_list():
    try:
        institution_id = request.args.get('institution_id')
        response = institution_service_obj.branch_list(institution_id)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/department_list", methods=["GET"])
def department_list():
    try:
        course_id = request.args.get('course_id')
        response = institution_service_obj.department_list(course_id)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/course_list", methods=["GET"])
def course_list():
    try:
        branch_id = request.args.get('branch_id')
        response = institution_service_obj.course_list(branch_id)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/institution_list", methods=["GET"])
def institution_list():
    try:
        response = institution_service_obj.institution_list()
        print("response", response)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/hard_skills_list", methods=["GET"])
@jwt_required()
def hard_skills_list():
    try:
        institution_id = None
        user_id = None
        current_user = get_jwt_identity()
        
        role_name = current_user["role_name"]
        if role_name == "Admin":
            institution_id = current_user["id"]
        else:
            user_id = current_user["id"]

        response = institution_service_obj.hard_skills_list(user_id, institution_id)
        print("response", response)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/soft_skills_list", methods=["GET"])
@jwt_required()
def soft_skills_list():
    try:
        institution_id = None
        user_id = None
        current_user = get_jwt_identity()
        
        role_name = current_user["role_name"]
        if role_name == "Admin":
            institution_id = current_user["id"]
        else:
            user_id = current_user["id"]

        response = institution_service_obj.soft_skills_list(user_id, institution_id)
        print("response", response)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# @institution_router.route("/interview_roles_list", methods=["GET"])
# def interview_roles_list():
#     try:
#         response = institution_service_obj.interview_roles_list()
#         print("response", response)
#         return jsonify(response)
    
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500

@institution_router.route("/companies_list", methods=["GET"])
@jwt_required()
def companies_list():
    try:
        institution_id = None
        user_id = None
        current_user = get_jwt_identity()
        
        role_name = current_user["role_name"]
        if role_name == "Admin":
            institution_id = current_user["id"]
        else:
            user_id = current_user["id"]
                    
        company_response = institution_service_obj.companies_list(user_id, institution_id)
        for company in company_response:
            roles_id_str = company["role_ids"]
            roles_id_list = roles_id_str.split(",")
            company["role_ids"] = institution_service_obj.get_interview_roles_list_names(roles_id_list, format='list(dict)')
        print("response", company_response)
        return jsonify(company_response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/reset_password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        validate(data, RESET_PASSWORD_SCHEMA)
        response = institution_service_obj.reset_password(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/update_password", methods=["POST"])
@jwt_required()
def update_password():
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        data = request.get_json()
        validate(data, INSTITUTION_UPDATE_PASSWORD_SCHEMA)
        response = institution_service_obj.update_password(data, user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@institution_router.route("/update", methods=["POST"])
@jwt_required()
def update_institution():
    try:
        institution_id = request.args.get('institution_id')
        data = request.get_json()
        validate(data, INSTITUTION_UPDATE_SCHEMA)    
        return jsonify(institution_service_obj.update_institution(institution_id, data))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@institution_router.route("/management", methods=["GET"])
@jwt_required()
def management():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        records = institution_service_obj.management(institution_id)
        return jsonify(records)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/list", methods=["GET"])
@jwt_required()
@requires_role("super admin")
def list_institutions():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        institutions = institution_service_obj.list_institutions_with_filters(institution_id)
        return jsonify(institutions)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/delete", methods=["DELETE"])
@jwt_required()
@requires_role("super admin")
def delete_institution():
    try:
        institution_id = request.args.get('institution_id')
        return jsonify(institution_service_obj.delete_institution(institution_id))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@institution_router.route("/<int:institution_id>/activate", methods=["GET"])
@jwt_required()
@requires_role("super admin")
def activate_institution(institution_id):
    try:
        return jsonify(institution_service_obj.activate_institution(institution_id))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/<int:institution_id>/deactivate", methods=["GET"])
@jwt_required()
@requires_role("super admin")
def deactive_institution(institution_id):
    try:
        return jsonify(institution_service_obj.deactive_institution(institution_id))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@institution_router.route("/deep_analysis/<analysis_mode>", methods=["GET"])
@jwt_required()
@requires_role("admin")
def deep_analysis(analysis_mode):
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        query_params = request.args.to_dict()
        validate(analysis_mode, ANALYSIS_MODE_SCHEMA)
        return jsonify(institution_service_obj.deep_analysis(analysis_mode, institution_id, query_params))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@institution_router.route("/statistics", methods=["GET"])
@jwt_required()
@requires_role("admin")
def institution_statistics():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        query_params = request.args.to_dict()
        return jsonify(institution_service_obj.institution_statistics(institution_id, query_params))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/update_interview_questions_mode", methods=["POST"])
@jwt_required()
@requires_role("admin")
def update_interview_questions_mode():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        query_params = request.args.to_dict()
        return jsonify(institution_service_obj.update_interview_questions_mode(institution_id, query_params))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/upload_configurations", methods=["POST"])
@jwt_required()
@requires_role("admin,teacher")
def upload_configurations():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        data = request.get_json()
        validate(data, INSTITUTION_CONFIGURATION_SCHEMA)    
        thread = threading.Thread(
            target=institution_service_obj.upload_configurations, 
            args=(institution_id, data,)
        )
        thread.start()
        return jsonify({"status": True, "message": "Configurations are uploaded and file is processing"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/download_configurations", methods=["GET"])
def download_configurations():
    try:
        access_token = request.args.get('access_token')
        mode = request.args.get('mode')
        parts = access_token.split('.')
        if len(parts) == 3:
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==').decode('utf-8'))
            payload = payload.get("sub", {})
            institution_id = payload.get('id', 0)
            
        response = institution_service_obj.download_configurations(institution_id, mode)
        if response.get("status"):
            file_name =  response["file_name"]
            data_dir = os.path.join(os.path.dirname(__file__), '')
            data_dir = data_dir.replace("/routes", "")
            file_path = os.path.join(data_dir, file_name)
            return send_file(file_path, as_attachment=True)
        else:
            sample_data = request.args.get('sample_data', False)
            mode = request.args.get('mode', '')
            data_dir = os.path.join(os.path.dirname(__file__), 'data/sample_upload_files')
            data_dir = data_dir.replace("/routes", "")
            file_name = download_sample_file(mode, sample_data)
            print("Filename", file_name)
            print("data_dir", data_dir)
            file_path = os.path.join(data_dir, file_name)
            return send_file(file_path, as_attachment=True)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@institution_router.route("/generate_screening_link", methods=["POST"])
@jwt_required()
@requires_role("admin")
def generate_screening_link():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        data = request.get_json()
        validate(data, GENERATE_SCREENING_LINK_SCHEMA)    
        return jsonify(institution_service_obj.generate_screening_link(data, institution_id))        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@institution_router.route("/screening_link_list", methods=["GET"])
@jwt_required()
@requires_role("admin")
def screening_link_list():
    try:
        current_user = get_jwt_identity()
        institution_id = current_user["id"]
        return jsonify(institution_service_obj.screening_link_list(institution_id))        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/screening/<screening_code>/active", methods=["GET"])
@jwt_required()
@requires_role("admin")
def screening_active(screening_code):
    try:
        return jsonify(institution_service_obj.screening_active(screening_code))        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/screening/<screening_code>/deactive", methods=["GET"])
@jwt_required()
@requires_role("admin")
def screening_deactive(screening_code):
    try:
        return jsonify(institution_service_obj.screening_deactive(screening_code))        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@institution_router.route("/screening_user_list", methods=["GET"])
@jwt_required()
@requires_role("admin")
def screening_user_list():
    try:
        screening_code = request.args.get('screening_code')
        return jsonify(institution_service_obj.screening_user_list(screening_code))        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@institution_router.route("/placement_tracker/<int:institution_id>", methods=["GET"])
# @jwt_required()
# @requires_role("admin")
def get_placement_tracker(institution_id):
    try:
        column_name = request.args.get('column_name', "created_date")
        order_by = request.args.get('order_by', 'DESC')
        page_number = int(request.args.get('page_number', 1))
        records_per_page = int(request.args.get('limit', 20))       
        return jsonify(institution_service_obj.get_placement_details(institution_id, column_name,order_by, page_number, records_per_page))        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


