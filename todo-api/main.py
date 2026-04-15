from flask import Flask, jsonify, request
import os
import json
from Task import Task   
import uuid 
from Exceptions import MyCustomError

app = Flask(__name__)

id1 = str(uuid.uuid4())
id2 = str(uuid.uuid4())

tasks = {
    id1: Task(uuid=id1, title="Buy groceries", description="Milk"),
    id2: Task(uuid=id2, title="Read a book", description="Gatsby")
}

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    if task_id not in tasks:
        raise MyCustomError("Task not found", error_code=404, payload={"id": task_id})
    
    return jsonify(tasks[task_id].to_dict())
        
@app.route('/tasks/title/<string:title>', methods=['GET']) 
def get_task_by_title(title):
    found_tasks = [task.to_dict() for task in tasks.values() if title.lower() in task.title.lower()]
    if not found_tasks:
        raise MyCustomError(f"No tasks found containing: {title}", error_code=404)
    return jsonify(found_tasks)

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify([task.to_dict() for task in tasks.values()])

@app.route('/tasks', methods=['POST'])
def create_task(): 
    data = request.get_json()
    if not data or 'title' not in data:
        raise MyCustomError("Title is required", error_code=400)

    new_id = str(uuid.uuid4())
    new_task = Task(uuid=new_id, title=data['title'], description=data.get('description', ""))
    tasks[new_id] = new_task
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks:
        raise MyCustomError("Task not found", error_code=404)
    
    data = request.get_json()
    task = tasks[task_id] 
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    
    return jsonify(task.to_dict())

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id] 
        return jsonify({"message": "Task deleted"}), 200
            
    raise MyCustomError("Task not found", error_code=404)

@app.errorhandler(MyCustomError)
def handle_custom_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.error_code
    return response

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    response = jsonify({"error": "An unexpected error occurred", "details": str(error)})
    response.status_code = 500
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)