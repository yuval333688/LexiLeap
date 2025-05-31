from User import User
from Lesson import Lesson
class Student(User):
    def __init__(self):
        super().__init__()  # Call User's constructor
        self.role = "Student"
        # Add student-specific attributes if needed, like:
        self.class_level = None  # or passed as input