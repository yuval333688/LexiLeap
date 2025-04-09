from datetime import time
from Question import Question
FINALS_LESSON_SESSIONS=20

class Lesson:
    def __init__(self,lesson_code: int, lesson_level: int, question_count: int):
        self.lesson_Code=lesson_code
        self.lesson_level = lesson_level
        self.question_count = FINALS_LESSON_SESSIONS
        self.questions[self.question_count]
        self.start_time = None
        self.end_time = None
        

    def setLesson(self):
         for i in range(FINALS_LESSON_SESSIONS):
             self.ques

   
    def run_lesson(self):
        print("Starting lesson...")
        self.start_time = datetime.now()

        for i, question in enumerate(self.questions, 1):
            print(f"\nQuestion {i}:")
            question.ask_question()

        self.end_time = datetime.now()
        duration = self.end_time - self.start_time
        print(f"\nLesson finished! Duration: {duration}")

    def __str__(self):
        return (f"Lesson(Level: {self.lesson_level}, Questions: {self.question_count}, "
                f"Start: {self.start_time}, End: {self.end_time})")

    def get_duration(self):
        """Returns the duration of the lesson in minutes."""
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return end_minutes - start_minutes

# Example usage
if __name__ == "__main__":
    lesson = Lesson(lesson_level=3, question_count=10, 
                    start_time=time(9, 0), end_time=time(10, 30))
    print(lesson)
    print("Duration:", lesson.get_duration(), "minutes")
