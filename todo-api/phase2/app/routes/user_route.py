from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    user_id = UserService.create_user(data)
    return jsonify({
        "message": "User registered successfully",
        "id": user_id  
    }), 201

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    return jsonify(user.to_dict()), 200

@user_bp.route('/<user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json() or {}
    UserService.update_user(user_id, data) 
    return jsonify({"message": "User updated successfully"}), 200

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserService.delete_user(user_id)
    return jsonify({
        "message": "User and all associated data deleted successfully",
        "details": result
    }), 200