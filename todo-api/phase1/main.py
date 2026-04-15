from flask import Flask, jsonify, request
import uuid
from Task import Task 
from Exceptions import MyCustomError

app = Flask(__name__)

# --- Initial Data Storage ---
id1, id2 = str(uuid.uuid4()), str(uuid.uuid4())
tasks = {
    id1: Task(uuid=id1, title="Learn Python", description="Study Flask and Exceptions"),
    id2: Task(uuid=id2, title="Build API", description="Integrate Swagger UI")
}

# --- Full CRUD Routes ---

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify([task.to_dict() for task in tasks.values()])

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    if task_id not in tasks:
        raise MyCustomError("Task not found", error_code=404, payload={"requested_id": task_id})
    return jsonify(tasks[task_id].to_dict())

@app.route('/tasks/search/<string:title>', methods=['GET'])
def search_tasks_by_title(title):
    found_tasks = [
        task.to_dict() for task in tasks.values() 
        if title.lower() in task.title.lower()
    ]

    if not found_tasks:
        raise MyCustomError(message=f"No tasks found containing the text: '{title}'", error_code=404, payload={"search_term": title})

    return jsonify(found_tasks)

@app.route('/tasks', methods=['POST'])
def create_task(): 
    data = request.get_json()
    validate_task_data(data)

    new_id = str(uuid.uuid4())
    new_task = Task(uuid=new_id, title=data['title'], description=data.get('description', ""))
    tasks[new_id] = new_task
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks:
        raise MyCustomError("Cannot update: Task not found", error_code=404)
    
    data = request.get_json()
    validate_task_data(data)
    
    task = tasks[task_id] 
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    
    return jsonify(task.to_dict())

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id not in tasks:
        raise MyCustomError("Cannot delete: Task not found", error_code=404) 
        
    del tasks[task_id] 
    return jsonify({"message": "Task deleted successfully"}), 200

# --- Global Error Handlers ---

@app.errorhandler(MyCustomError)
def handle_custom_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.error_code
    return response

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    response = jsonify({"status": "error","message": "Internal Server Error","details": str(error)})
    response.status_code = 500
    return response

def validate_task_data(data):
    if not data or 'title' not in data:
        raise MyCustomError("Missing field: 'title'", error_code=400)
    if not data['title'].strip():
        raise MyCustomError("Field 'title' cannot be empty", error_code=400)
    if 'description' in data and not data['description'].strip():
        raise MyCustomError("Field 'description' cannot be empty", error_code=400)

if __name__ == "__main__":
    app.run(debug=True, port=5000)