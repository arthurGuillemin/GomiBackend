from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.supabase import get_user_by_id, get_username_by_id, update_user, delete_user

user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/<string:user_id>', methods=['GET'])
@jwt_required()
def getUserById(user_id):
    result = get_user_by_id(user_id)
    return jsonify(result)

@user_routes.route('/<string:user_id>/name', methods=['GET'])
@jwt_required()
def getUserNameById(user_id):
    result = get_username_by_id(user_id)
    return jsonify(result)

@user_routes.route('/<string:user_id>', methods=['DELETE'])
@jwt_required()
def deleteUser(user_id):
    result = delete_user(user_id)
    return jsonify(result)

@user_routes.route('/<string:user_id>', methods=['PUT'])
@jwt_required()
def updateUser(user_id):
    data = request.json
    if not data:
        return jsonify({"error": "Aucune donnée fournie"}), 400
    result = update_user(user_id, data)
    return jsonify(result)
