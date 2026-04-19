from flask import Blueprint, request, jsonify
from services.task_service import TaskService

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks', methods=['POST'])
def create():
    task_id = TaskService.create_task(request.get_json())
    return jsonify({"message": "Task created", "id": task_id}), 201

@task_bp.route('/tasks', methods=['GET'])
def get_all():
    user_id = request.headers.get('User-ID') 
    if not user_id:
        return jsonify({"error": "User-ID is missing"}), 400
    
    tasks = TaskService.get_tasks_by_user_id(user_id) 
    
    for task in tasks:
        task['_id'] = str(task['_id'])
        
    return jsonify({"tasks": tasks}), 200

@task_bp.route('/tasks/<task_id>', methods=['GET'])
def get_one(task_id):
    task = TaskService.get_task_by_id(task_id)
    task['_id'] = str(task['_id'])
    return jsonify({"task": task}), 200

@task_bp.route('/tasks/<task_id>', methods=['PUT'])
def update(task_id):
    TaskService.update_task(task_id, request.get_json())
    return jsonify({"message": "Task updated"}), 200

@task_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete(task_id):
    TaskService.delete_task(task_id)
    return jsonify({"message": "Task deleted"}), 200

@task_bp.route('/categories/<category_id>/tasks', methods=['GET'])
def get_tasks_by_category(category_id):
    tasks = TaskService.get_tasks_by_category(category_id)
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify({"tasks": tasks}), 200