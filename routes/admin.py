import logging
import traceback
import os
import io

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# from jsonschema import validate
from services import AdminService
# Harnath Need to add validation
# from validation import CREATE_ASSIGNMENT_SCHEMA, ASSIGN_ASSIGNMENT_SCHEMA, UNASSIGN_ASSIGNMENT_SCHEMA, UPDATE_ASSIGNMENT_SCHEMA
from access_check import requires_role

admin_router = Blueprint("admin", __name__)
logger = logging.getLogger("admin")

admin_service_obj = AdminService()

@admin_router.route("/entity/create", methods=["POST"])
def create_entity():
    try:
        data = request.get_json()
        entity = admin_service_obj.create_entity(data)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@admin_router.route("/entity/mapping", methods=["POST"])
def create_entity_mapping():
    try:
        data = request.get_json()
        entity = admin_service_obj.create_entity_mapping(data)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@admin_router.route("/entity/list", methods=["GET"])
def entity_list():
    try:
        data = request.get_json()
        entity = admin_service_obj.get_entity_list(data)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@admin_router.route("/entity/mapping/<entity_name>", methods=["GET"])
def entity_mapping(entity_name):
    try:
        entity = admin_service_obj.get_entity_mapping(entity_name)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@admin_router.route("/entity/activate/<int:entity_id>", methods=["PUT"])
def activate_entity(entity_id):
    try:
        entity = admin_service_obj.activate_entity(entity_id)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@admin_router.route("/entity/deactivate/<int:entity_id>", methods=["PUT"])
def deactivate_entity(entity_id):
    try:
        entity = admin_service_obj.deactivate_entity(entity_id)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

@admin_router.route("/entity_mapping/activate/<int:entity_mapping_id>", methods=["PUT"])
def activate_entity_mapping(entity_mapping_id):
    try:
        entity = admin_service_obj.activate_entity_mapping(entity_mapping_id)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@admin_router.route("/entity_mapping/deactivate/<int:entity_mapping_id>", methods=["PUT"])
def deactivate_entity_mapping(entity_mapping_id):
    try:
        entity = admin_service_obj.deactivate_entity_mapping(entity_mapping_id)
        return jsonify(entity)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    


@admin_router.route("/generate_questions", methods=["POST"])
def generate_skill_questions():
    try:
        data = request.get_json()
        response = admin_service_obj.generate_skill_questions(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

