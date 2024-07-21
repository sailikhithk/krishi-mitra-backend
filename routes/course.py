import logging
import traceback

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from jsonschema import validate
from services import CourseService
from validation import CREATE_COURSE_SCHEMA, ASSIGN_COURSE_SCHEMA,UNASSIGN_COURSE_SCHEMA,CREATE_COURSE_CONTENT_SCHEMA, UPDATE_TRACK_COURSE_CONTENT_SCHEMA
from access_check import requires_role

course_router = Blueprint("course", __name__)
logger = logging.getLogger("course")

course_service_obj = CourseService()

@course_router.route("/create", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def create_course():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        data = request.get_json()
        validate(data, CREATE_COURSE_SCHEMA)
        response = course_service_obj.create_course(data, user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/get/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        response = course_service_obj.get_course(course_id, user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/list", methods=["GET"])
@jwt_required()
@requires_role("teacher,student")
def list_course():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        user_role = current_user["role_name"]
        response = course_service_obj.list_course(user_id, user_role)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/assign", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def assign_course():
    try:
        data = request.get_json()
        validate(data, ASSIGN_COURSE_SCHEMA)
        response = course_service_obj.assign_course(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/unassign", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def unassign_course():
    try:
        data = request.get_json()
        validate(data, UNASSIGN_COURSE_SCHEMA)
        response = course_service_obj.unassign_course(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/get_users/<int:course_id>", methods=["GET"])
@jwt_required()
@requires_role("teacher")
def get_users(course_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        branch_name = current_user.get("branch_name")
        institution_id = current_user.get("institution_id")

        response = course_service_obj.get_users(course_id, institution_id, branch_name)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/create_content", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def create_content():
    try:
        data = request.get_json()
        validate(data, CREATE_COURSE_CONTENT_SCHEMA)
        response = course_service_obj.create_content(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/delete/<int:course_id>", methods=["DELETE"])
@jwt_required()
@requires_role("teacher")
def delete_course(course_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        response = course_service_obj.delete_course(course_id, user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@course_router.route("/update_task", methods=["POST"])
@jwt_required()
@requires_role("student")
def update_task():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        data = request.get_json()
        print("data", data)
        # validate(data, UPDATE_TRACK_COURSE_CONTENT_SCHEMA)
        
        response = course_service_obj.update_task(data, user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

