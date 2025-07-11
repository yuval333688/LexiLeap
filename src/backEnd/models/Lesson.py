from datetime import datetime,time
from src.backEnd.models.Test import Test
import pandas as pd
from src.backEnd.models.Word import Word
import json
FINALS_TESTS_NUM = 19
FINALS_WORDS_IN_TEST=20
class Lesson:
 _lesson_counter = 1  # Class variable to ensure unique test codes
 def __init__(self,sudent_id):
            file_path = r"C:\Users\User\OneDrive\שולחן העבודה\Work\פרויקט גמר\tamp\LexiLeap\rec\worlds\lesson3.txt"
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                # Tokenize words
            words = text.split()
            # Take the all words as strings
            self.all_strings = words[:FINALS_TESTS_NUM * FINALS_WORDS_IN_TEST]  
            self.student_lesson = sudent_id 
            Lesson.lesson_serial_num= Lesson._lesson_counter
            Lesson._lesson_counter += 1
            self.tests = []##array of all tests
            self.setLesson()
        
 def setLesson(self):   
        for i_test in range(FINALS_TESTS_NUM):
            words_for_test=[]
            for i_words in range(FINALS_WORDS_IN_TEST):
                word_index = i_test * FINALS_WORDS_IN_TEST+i_words
                if word_index >= len(self.all_strings):
                    break
                word_str = self.all_strings[word_index]
                words_for_test.append(Word(word_str))
            self.tests.append(Test(words=words_for_test))
            
 def getTestByNum(self,test_num: int):
        """Returns list of words from the test as JSON"""
        test = self.tests[test_num - 1]
        # Assuming Word has a `.word` attribute; change if needed
        words_list = [q.word.word for q in test.questions]  # q is a Question
        return json.dumps(words_list, ensure_ascii=False, indent=2)
            
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
 
 
def getTestByNum(self, test_num: int):
        return [q.word.word for q in self.tests[test_num - 1].questions]