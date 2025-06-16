from flask import Flask, jsonify, request
import json
from models.Student import Student

app = Flask(__name__)
STUDENT_JSON_PATH = "students_data.json"

# Load all students from file
def load_students():
    try:
        with open(STUDENT_JSON_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save all students to file
def save_students(data):
    with open(STUDENT_JSON_PATH, 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/student", methods=["POST"])
def create_student():
    data = request.json
    try:
        student = Student(
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            user_id=data["user_id"],
            date_of_birth=data["date_of_birth"],
            class_level=data.get("class_level")
        )
        
        students = load_students()
        students[student.user_id] = {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "date_of_birth": student.date_of_birth,
            "class_level": student.class_level,
            "role": student.role
        }
        save_students(students)
        return jsonify({"message": "Student created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/student/<user_id>", methods=["GET"])
def get_student(user_id):
    students = load_students()
    student = students.get(user_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)

if __name__ == "__main__":
    app.run(debug=True)
