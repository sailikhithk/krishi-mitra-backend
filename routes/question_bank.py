import logging
import traceback

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from jsonschema import validate
from services import QuestionBankService
from validation import PROCESS_QUESTION_BANK_REQUEST,CREATE_QUESTION_BANK_SCHEME
from access_check import requires_role

question_bank_router = Blueprint("question_bank", __name__)
logger = logging.getLogger("question_bank")

question_bank_service_obj = QuestionBankService()

@question_bank_router.route("/process_request", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def process_request():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        
        data = request.get_json()
        validate(data, PROCESS_QUESTION_BANK_REQUEST)    
        user = question_bank_service_obj.process_request(data, user_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@question_bank_router.route("/create", methods=["POST"])
@jwt_required()
@requires_role("teacher")
def create_question_bank():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        
        data = request.get_json()
        validate(data, CREATE_QUESTION_BANK_SCHEME)    

        user = question_bank_service_obj.create_question_bank(data, user_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@question_bank_router.route("/get/<int:question_bank_id>", methods=["GET"])
@jwt_required()
def get_question_bank(question_bank_id):
    try:
        user = question_bank_service_obj.get_question_bank(question_bank_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@question_bank_router.route("/list", methods=["GET"])
@jwt_required()
@requires_role("teacher")
def list_question_bank():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")

        user = question_bank_service_obj.list_question_bank(user_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@question_bank_router.route("/delete/<int:question_bank_id>", methods=["DELETE"])
@jwt_required()
@requires_role("teacher")
def delete_question_bank(question_bank_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        user = question_bank_service_obj.delete_question_bank(question_bank_id)
        return jsonify(user)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500










