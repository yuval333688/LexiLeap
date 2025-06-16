# models/Teacher.py
from src.backEnd.models.User import User

class Teacher(User):
    def __init__(self, password, first_name, last_name, user_id, date_of_birth, subject=None):
        super().__init__(password, first_name, last_name, user_id, date_of_birth)
        self.role = "Teacher"
      
