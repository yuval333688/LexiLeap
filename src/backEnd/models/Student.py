# models/Student.py
from src.backEnd.models.User import User
from src.backEnd.models.Lesson import Lesson
from src.backEnd.models.Teacher import Teacher

studant_lesson=Lesson()
class Student(User):
    def __init__(self, password, first_name, last_name, user_id, date_of_birth, class_level=None):
        super().__init__(password, first_name, last_name, user_id, date_of_birth)
        self.role = "Student"
        self.class_level = class_level  # Optional
        self.Student_lesson=Lesson(user_id)
        self.Student_teacher=Teacher()
