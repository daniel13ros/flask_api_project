from flask import Flask, jsonify, request
import os
import json
from Student import Student  # Import once at the top

app = Flask(__name__)
data_file = 'student api/students_db.json'

# --- Data Persistence Helpers ---

def load_data():
    if not os.path.exists(data_file):
        return []
    with open(data_file, 'r') as f:
        return json.load(f)
    
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

# --- Routes: General ---

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Student API!"})

@app.route('/students', methods=['GET'])
def get_all_students():
    return jsonify(load_data())

@app.route('/students', methods=['POST'])
def add_student():
    new_student_data = request.get_json()
    students = load_data()
    
    try:
        temp_student = Student(**new_student_data)
        students.append(temp_student.to_dict())
        save_data(students)
        return jsonify({"message": "Student added successfully!", "student": temp_student.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- Routes: Individual Student Management ---

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    students = load_data()
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found!"}), 404

@app.route('/students/<int:student_id>', methods=['PUT'])
@app.route('/students/<int:student_id>/info', methods=['PUT'])
def update_student(student_id):
    updated_info = request.get_json()
    students = load_data()
    
    updated_info.pop('id', None)
    for student in students:
        if student['id'] == student_id:
            temp_student = Student(**student)
            temp_student.update_info(**updated_info)
            student.update(temp_student.to_dict())
            save_data(students)
            return jsonify({"message": "Student updated successfully!", "student": temp_student.to_dict()})
    
    return jsonify({"error": "Student not found!"}), 404

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    students = load_data()
    original_length = len(students)
    students = [s for s in students if s['id'] != student_id]
    
    if len(students) < original_length:
        save_data(students)
        return jsonify({"message": "Student deleted successfully!"})
    
    return jsonify({"error": "Student not found!"}), 404

# --- Routes: Academic & Stats ---

@app.route('/students/<int:student_id>/gpa', methods=['GET'])
def get_gpa(student_id):
    students = load_data()
    student_data = next((s for s in students if s['id'] == student_id), None)
    
    if student_data:
        temp_student = Student(**student_data)
        return jsonify({"id": student_id,"name": f"{temp_student.fname} {temp_student.lname}", "gpa": temp_student.get_gpa()})
    return jsonify({"error": "Student not found!"}), 404

@app.route('/students/<int:student_id>/status', methods=['GET'])
def get_status(student_id):
    students = load_data()
    student_data = next((s for s in students if s['id'] == student_id), None)
    
    if student_data:
        temp_student = Student(**student_data)
        return jsonify({"id": student_id, "academic_status": temp_student.get_academic_status()})
    return jsonify({"error": "Student not found!"}), 404

# --- Routes: Course Management ---

@app.route('/students/<int:student_id>/courses', methods=['GET'])
def get_courses(student_id):
    students = load_data()
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify({"courses": student.get('courses', [])})
    return jsonify({"error": "Student not found!"}), 404

@app.route('/students/<int:student_id>/courses', methods=['POST'])
def add_course(student_id):
    course_obj = request.get_json() 
    students = load_data()
    
    for student in students:
        if student['id'] == student_id:
            temp_student = Student(**student)
            temp_student.add_course(course_obj)
            student.update(temp_student.to_dict())
            save_data(students)
            return jsonify({"message": "Course added!", "student": temp_student.to_dict()})
    return jsonify({"error": "Student not found!"}), 404

@app.route('/students/<int:student_id>/courses', methods=['PUT'])
def edit_course(student_id):
    data = request.get_json()
    students = load_data()
    
    for student in students:
        if student['id'] == student_id:
            temp_student = Student(**student)
            temp_student.edit_course(data.get('old_name'), data.get('new_course'))
            student.update(temp_student.to_dict())
            save_data(students)
            return jsonify({"message": "Course updated!", "student": temp_student.to_dict()})
    return jsonify({"error": "Student not found!"}), 404

@app.route('/students/<int:student_id>/courses', methods=['DELETE'])
def remove_course(student_id):
    course_to_remove = request.get_json() 
    students = load_data()
    
    for student in students:
        if student['id'] == student_id:
            temp_student = Student(**student)
            target = next((c for c in temp_student.courses if c['name'] == course_to_remove.get('name')), None)
            if target:
                temp_student.remove_course(target)
                student.update(temp_student.to_dict())
                save_data(students)
                return jsonify({"message": "Course removed!"})
            return jsonify({"error": "Course not found in student list!"}), 404
            
    return jsonify({"error": "Student not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True , port = 5000)