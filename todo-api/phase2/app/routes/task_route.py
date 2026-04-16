from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    task_id = TaskService.create_task(data)
    return jsonify({
        "message": "Task created successfully",
        "id": task_id
    }), 201

@task_bp.route('/user/<user_id>', methods=['GET'])
def get_user_tasks(user_id):
    tasks = TaskService.get_all_tasks(user_id)
    return jsonify(tasks), 200

@task_bp.route('/search/<user_id>', methods=['GET'])
def search_tasks(user_id):
    title_query = request.args.get('title', '')
    tasks = TaskService.get_tasks_by_user_id_and_title(user_id, title_query)
    return jsonify(tasks), 200

@task_bp.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    task = TaskService.get_task_by_id(task_id)
    return jsonify(task.to_dict()), 200

@task_bp.route('/<task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.get_json() or {}
    TaskService.update_task(task_id, data)
    return jsonify({"message": "Task updated successfully"}), 200

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    TaskService.delete_task(task_id)
    return jsonify({"message": "Task deleted successfully"}), 200