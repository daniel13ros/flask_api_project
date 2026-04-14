from flask import Flask, jsonify, request
import os
import json
from Task import Task   
import uuid 

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
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(tasks[task_id].to_dict())

@app.route('/tasks/title/<string:title>', methods=['GET'])
def get_task_by_title(title):
    found_tasks = [task.to_dict() for task in tasks.values() if title.lower() in task.title.lower()]
    if not found_tasks:
        return jsonify({"error": "No tasks found with that title"}), 404
    return jsonify(found_tasks)

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify([task.to_dict() for task in tasks.values()])

@app.route('/tasks', methods=['POST'])
def create_task(): 
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Missing 'title' in request"}), 400

    new_id = str(uuid.uuid4())
    new_task = Task(id=new_id, title=data['title'], description=data.get('description', ""))
    tasks[new_id] = new_task
    
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    
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
            
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)