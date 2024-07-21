import logging
import traceback

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from jsonschema import validate
from services import AssignmentService
# Harnath Need to add validation
from validation import CREATE_ASSIGNMENT_SCHEMA, ASSIGN_ASSIGNMENT_SCHEMA, UNASSIGN_ASSIGNMENT_SCHEMA, UPDATE_ASSIGNMENT_SCHEMA, SUBMIT_ASSIGNMENT_SCHEMA
from access_check import requires_role

assignment_router = Blueprint("assignment", __name__)
logger = logging.getLogger("assignment")

assignment_service_obj = AssignmentService()

@assignment_router.route("/create", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def create_assignment():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        data = request.get_json()
        validate(data, CREATE_ASSIGNMENT_SCHEMA)
        user = assignment_service_obj.create_assignment(data, user_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/assign", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def assign_assignment():
    try:
        data = request.get_json()
        validate(data, ASSIGN_ASSIGNMENT_SCHEMA)
        user = assignment_service_obj.assign_assignment(data)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/update", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def update_assignment():
    try:
        data = request.get_json()
        validate(data, UPDATE_ASSIGNMENT_SCHEMA)
        user = assignment_service_obj.update_assignment(data)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/unassign", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def unassign_assignment():
    try:
        data = request.get_json()
        validate(data, UNASSIGN_ASSIGNMENT_SCHEMA)
        user = assignment_service_obj.unassign_assignment(data)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/get_users/<int:assignment_id>", methods=["GET"])
@jwt_required()
@requires_role("teacher")
def get_users(assignment_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        branch_name = current_user.get("branch_name")
        institution_id = current_user.get("institution_id")

        response = assignment_service_obj.get_users(assignment_id, institution_id, branch_name)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/get/<int:assignment_id>", methods=["GET"])
@jwt_required()
def get_assignment(assignment_id):
    try:
        user = assignment_service_obj.get_assignment(assignment_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/delete/<int:assignment_id>", methods=["DELETE"])
@jwt_required()
@requires_role("teacher")
def delete_assignment(assignment_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        user = assignment_service_obj.delete_assignment(assignment_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/list", methods=["GET"])
@jwt_required()
@requires_role("teacher,student")
def list_assignment():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        user_role_name = str(current_user.get("role_name", "")).strip().lower()

        user = assignment_service_obj.list_assignment(user_id, user_role_name)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

@assignment_router.route("/start/<int:assignment_id>", methods=["GET"])
@jwt_required()
@requires_role("student")
def start_assignment(assignment_id):
    try:
        user = assignment_service_obj.start_assignment(assignment_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/results/<int:assignment_id>", methods=["GET"])
@jwt_required()
@requires_role("teacher,student")
def assignment_results(assignment_id):
    try:
        user = assignment_service_obj.assignment_results(assignment_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@assignment_router.route("/submit", methods=["POST"])
@jwt_required()
@requires_role("student")
def submit_assignment():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        data = request.get_json()
        validate(data, SUBMIT_ASSIGNMENT_SCHEMA)
        response = assignment_service_obj.submit_assignment(data,user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

@assignment_router.route("/is_assignment_allowed/<int:assignment_id>", methods=["GET"])
@jwt_required("student")
def is_assignment_allowed(assignment_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        response = assignment_service_obj.is_assignment_allowed(assignment_id, user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

