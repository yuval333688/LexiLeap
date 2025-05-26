from datetime import datetime,time
from Question import Question
import pandas as pd

from src.backEnd.Word import Word
FINALS_LESSON_SESSIONS = 20


class Lesson:
 
 _test_counter = 0  # Class variable to ensure unique test codes
 
 def __init__(self,lesson_code: int, level: int):
        self.test_code = Lesson._test_counter
        Lesson._test_counter += 1
        self.level =level
        self.question_count = FINALS_LESSON_SESSIONS
        self.questions = []
        self.setLesson(test_loader)
        self.start_time = None
        self.end_time = None
        
 def setLesson(self, test_loader: list[str]):
        """Sets up questions for the lesson using modulo skipping strategy."""
        self.questions = []
        total_words = len(test_loader)

        for i in range(self.question_count):
            index = self.level + i * FINALS_LESSON_SESSIONS
            if index >= total_words:
                break
            word_str = test_loader[index]
            word = Word(word_str)
            question = Question(word)
            self.questions.append(question)
            
 def getLesson(self):
        return self.questions
            
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
        return (f"Lesson(Test Code: {self.test_code}, Level: {self.level}, "
                f"Questions: {self.question_count}, "
                f"Start: {self.start_time}, End: {self.end_time})")

 def __repr__(self):
        return f"Lesson(Level: {self.level}, Questions: {self.questions})"

 def get_duration(self):
        """Returns the duration of the lesson in minutes."""
        if not self.start_time or not self.end_time:
            return 0
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return end_minutes - start_minutes