from flask import Blueprint, request, jsonify
from backEnd.models.Teacher import Teacher

teacher_api = Blueprint("teacher_api", __name__)

@teacher_api.route("/register", methods=["POST"])
def register_teacher():
    data = request.get_json()
    try:
        teacher = Teacher(**data)
        return jsonify({
            "message": "Teacher created!",
            "username": teacher.user_name,
            "role": teacher.role
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
