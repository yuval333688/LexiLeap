from User import User


class Teacher(User):
    def __init__(self):
        super().__init__()
        self.role = "Teacher"
        # Add teacher-specific attributes if needed, like:
        self.subjects = []  # or passed as input