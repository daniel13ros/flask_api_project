from flask import  Blueprint,request, jsonify
from services.user_service import UserService
from services.task_service import TaskService

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create():
    user_id = UserService.create_user(request.get_json())
    return jsonify({"message": "User created", "id": user_id}), 201

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_one(user_id):
    user = UserService.get_user_by_id(user_id)
    user['_id'] = str(user['_id'])
    return jsonify({"user": user}), 200

@user_bp.route('/users', methods=['GET'])
def get_all():
    users = UserService.get_all_users()
    
    for user in users:
        user['_id'] = str(user['_id'])
        
    return jsonify({"users": users}), 200

@user_bp.route('/users/<user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    tasks = TaskService.get_tasks_by_user_id(user_id)
    
    for task in tasks:
        task['_id'] = str(task['_id'])
        
    return jsonify({"tasks": tasks}), 200

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update(user_id):
    UserService.update_user(user_id, request.get_json())
    return jsonify({"message": "User updated"}), 200

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete(user_id):
    UserService.delete_user(user_id)
    return jsonify({"message": "User deleted"}), 200