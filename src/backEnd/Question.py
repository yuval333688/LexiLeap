from Word import Word
import Levenshtein
FINALS_WRONG_CHAR = -10 
FINALS_CORRECT_WORD = 100
# Define a 26x26 matrix for the distance between any two characters
keyboard_distance = {
                    ('a', 'a'):0, ('a', 'b'):5, ('a', 'c'):3, ('a', 'd'):2, ('a', 'e'):2, ('a', 'f'):3, ('a', 'g'):4 ,('a', 'h'):5,('a', 'i'):7,('a', 'j'):6,('a', 'k'):7,('a', 'l'):8,('a', 'm'):7,('a', 'n'):6,('a', 'o'):8,('a', 'p'):9,('a', 'q'):1,('a', 'r'):3,('a', 's'):1,('a', 't'):4,('a', 'u'):6,('a', 'v'):4,('a', 'w'):1,('a', 'x'):2,('a', 'y'):5,('a', 'z'):1,                
                    ('b', 'b'): 0,('b', 'c'):2, ('b', 'd'): 3,('b', 'e'): 4, ('b', 'f'): 2, ('b', 'g'): 1, ('b', 'h'): 1, ('b', 'i'): 3, ('b', 'j'): 2,    ('b', 'k'): 3, ('b', 'l'): 4, ('b', 'm'): 2, ('b', 'n'): 1, ('b', 'o'): 4,    ('b', 'p'): 5, ('b', 'q'): 6, ('b', 'r'): 3, ('b', 's'): 4, ('b', 't'): 2,    ('b', 'u'): 2, ('b', 'v'): 1, ('b', 'w'): 5, ('b', 'x'): 3, ('b', 'y'): 2, ('b', 'z'): 4,
                    ('c', 'c'): 0,('c', 'd'): 1,('c', 'e'): 2,('c', 'f'): 1, ('c', 'g'): 2,('c', 'h'): 3,('c', 'i'): 5,('c', 'j'): 4,('c', 'k'): 5,('c', 'l'): 6, ('c', 'm'): 4, ('c', 'n'): 3, ('c', 'o'): 6,('c', 'p'): 7, ('c', 'q'): 4, ('c', 'r'): 2, ('c', 's'): 2, ('c', 't'): 2,('c', 'u'): 4, ('c', 'v'): 1, ('c', 'w'): 3, ('c', 'x'): 1, ('c', 'y'): 3,('c', 'z'): 2,   
                    ('d', 'd'): 0,('d', 'e'):1, ('d', 'f'): 1,('d', 'g'): 2,('d', 'h'): 3,('d', 'i'):5,('d', 'j'): 4,    ('d', 'k'):5 ,    ('d', 'l'):6,    ('d', 'm'):5,    ('d', 'n'): 4, ('d', 'o'): 6,   ('d', 'p'): 7,   ('d', 'q'): 3,    ('d', 'r'): 1,    ('d', 's'): 1,    ('d', 't'): 2,   ('d', 'u'): 4,    ('d', 'v'): 2,    ('d', 'w'): 2,    ('d', 'x'): 1,    ('d', 'y'): 3,    ('d', 'z'): 2,
                    ('e', 'e'): 0,('e', 'f'): 2,('e', 'g'): 3,('e', 'h'): 4,('e', 'i'): 6,('e', 'j'): 5,    ('e', 'k'): 6,    ('e', 'l'):7 ,    ('e', 'm'): 6,    ('e', 'n'):5 ,    ('e', 'o'): 6,('e', 'p'):7 ,('e', 'q'): 2,('e', 'r'):1 ,    ('e', 's'): 1,    ('e', 't'):2 ,    ('e', 'u'): 4,    ('e', 'v'): 3,    ('e', 'w'):1 ,    ('e', 'x'): 2,    ('e', 'y'):3 ,    ('e', 'z'): 2,
                    ('f', 'f'): 0,('f', 'g'): 1,('f', 'h'): 2,('f', 'i'):4 ,('f', 'j'): 3,('f', 'k'):4 ,('f', 'l'): 5, ('f', 'm'):4 , ('f', 'n'): 3, ('f', 'o'): 5,    ('f', 'p'): 6,    ('f', 'q'):4 ,    ('f', 'r'): 1,    ('f', 's'):2 ,    ('f', 't'):1 ,    ('f', 'u'):3 ,    ('f', 'v'): 1,    ('f', 'w'): 3,    ('f', 'x'): 2,    ('f', 'y'): 2, ('f', 'z'): 3,
                    ('g', 'g'): 0,('g', 'h'):1 ,('g', 'i'): 3,('g', 'j'): 2,('g', 'k'): 3,('g', 'l'): 4,    ('g', 'm'):3 ,    ('g', 'n'): 2,    ('g', 'o'):4 ,    ('g', 'p'): 5, ('g', 'q'): 5,    ('g', 'r'):2 ,    ('g', 's'): 3,    ('g', 't'): 1,    ('g', 'u'): 2,    ('g', 'v'): 1,    ('g', 'w'): 4,    ('g', 'x'): 3,    ('g', 'y'): 1,    ('g', 'z'): 4,
                    ('h', 'h'): 0,('h', 'i'):2, ('h', 'j'):1, ('h', 'k'):2,('h', 'l'): 3,('h', 'm'): 2,  ('h', 'n'): 1,    ('h', 'o'): 3,    ('h', 'p'): 4,  ('h', 'q'): 6,    ('h', 'r'): 3,    ('h', 's'): 4,('h', 't'): 2,    ('h', 'u'): 1, ('h', 'v'): 2,    ('h', 'w'): 5,    ('h', 'x'): 4,    ('h', 'y'):1 ,    ('h', 'z'): 5,
                    ('i', 'i'): 0,('i', 'j'):1, ('i', 'k'):1, ('i', 'l'):2,('i', 'm'):2 ,('i', 'n'):2 ,    ('i', 'o'):1 ,    ('i', 'p'): 2,    ('i', 'q'):7 ,    ('i', 'r'):4 ,    ('i', 's'): 6,    ('i', 't'): 3,    ('i', 'u'): 1,    ('i', 'v'): 4,    ('i', 'w'): 6,    ('i', 'x'): 6,    ('i', 'y'): 2,    ('i', 'z'): 7,
                    ('j', 'j'): 0,('j', 'k'):1, ('j', 'l'):2, ('j', 'm'):1,('j', 'n'):1 ,('j', 'o'): 2,    ('j', 'p'): 3,    ('j', 'q'):7 ,    ('j', 'r'): 4,    ('j', 's'): 5,    ('j', 't'): 3,    ('j', 'u'): 1,    ('j', 'v'): 3,    ('j', 'w'): 6,    ('j', 'x'): 5,    ('j', 'y'): 2,    ('j', 'z'): 6,
                    ('k', 'k'): 0,('k', 'l'):1, ('k', 'm'):1,('k', 'n'):2,('k', 'o'): 1, ('k', 'p'): 2,    ('k', 'q'): 8,    ('k', 'r'): 5,    ('k', 's'): 6,    ('k', 't'): 4,    ('k', 'u'): 2,    ('k', 'v'): 4,    ('k', 'w'): 7,    ('k', 'x'): 6,    ('k', 'y'): 3,    ('k', 'z'): 7,
                    ('l', 'l'): 0,('l', 'm'):2, ('l', 'n'):3, ('l', 'o'):1,('l', 'p'): 1, ('l', 'q'):9 ,    ('l', 'r'):6 ,    ('l', 's'): 7,    ('l', 't'): 5,    ('l', 'u'): 3,    ('l', 'v'): 5,    ('l', 'w'): 8,    ('l', 'x'): 7,    ('l', 'y'): 4,    ('l', 'z'): 8,
                    ('m', 'm'): 0,('m', 'n'):1, ('m', 'o'):2, ('m', 'p'):3,('m', 'q'): 8, ('m', 'r'): 5,    ('m', 's'):6 ,    ('m', 't'): 4,    ('m', 'u'): 2, ('m', 'v'): 3, ('m', 'w'): 7,    ('m', 'x'): 5,    ('m', 'y'): 3,    ('m', 'z'): 6,
                    ('n', 'n'): 0,('n', 'o'):3, ('n', 'p'):4, ('n', 'q'):7,('n', 'r'):4 , ('n', 's'): 5,    ('n', 't'): 3,    ('n', 'u'): 2,    ('n', 'v'): 2,    ('n', 'w'): 6,    ('n', 'x'): 4,    ('n', 'y'): 2,    ('n', 'z'): 5,
                    ('o', 'o'): 0,('o', 'p'):1, ('o', 'q'):8, ('o', 'r'):5,('o', 's'): 7, ('o', 't'): 4,    ('o', 'u'): 2,    ('o', 'v'): 5,    ('o', 'w'): 7,    ('o', 'x'): 7,    ('o', 'y'): 3,    ('o', 'z'): 8,
                    ('p', 'p'): 0,('p', 'q'):9, ('p', 'r'):6, ('p', 's'):8,('p', 't'): 5, ('p', 'u'): 3,    ('p', 'v'): 6,    ('p', 'w'): 8,    ('p', 'x'): 8,    ('p', 'y'): 4,    ('p', 'z'): 9,
                    ('q', 'q'): 0,('q', 'r'):3, ('q', 's'):2, ('q', 't'):4,('q', 'u'): 6, ('q', 'v'): 5,    ('q', 'w'): 1,    ('q', 'x'): 3,    ('q', 'y'): 5,    ('q', 'z'): 2,
                    ('r', 'r'): 0,('r', 's'):2, ('r', 't'):1, ('r', 'u'):3,('r', 'v'): 2, ('r', 'w'): 2,    ('r', 'x'): 2,    ('r', 'y'): 2,    ('r', 'z'): 3,
                    ('s', 's'): 0,('s', 't'):3, ('s', 'u'):5, ('s', 'v'):3,('s', 'w'): 1, ('s', 'x'): 1,    ('s', 'y'): 4,    ('s', 'z'): 1,
                    ('t', 't'): 0,('t', 'u'):2, ('t', 'v'):2, ('t', 'w'):3,('t', 'x'):3 , ('t', 'y'): 1,    ('t', 'z'): 4,
                    ('u', 'u'): 0,('u', 'v'):3, ('u', 'w'):5, ('u', 'x'):5,('u', 'y'):1 , ('u', 'z'): 6,
                    ('v', 'v'): 0,('v', 'w'):4, ('v', 'x'):2,('v', 'y'):2,('v', 'z'): 3,
                    ('w', 'w'): 0,('w', 'x'):2, ('w', 'y'):4,('w', 'z'):2,
                    ('x', 'x'): 0,('x', 'y'):4, ('x', 'z'):1,
                    ('y', 'y'): 0,('y', 'z'):5,
                    ('z', 'z'):0
                }

# Function to calculate the "neighbor distance" based on the custom matrix
def get_keyboard_distance(char1, char2):
    char1 = char1.lower()
    uniOfChar1=ord(char1)
    char2 = char2.lower()
    uniOfChar2=ord(char2)
    if  (uniOfChar1<uniOfChar2):
        return 10-keyboard_distance.get((char1, char2),FINALS_WRONG_CHAR) 
    return 10-keyboard_distance.get((char2, char1),FINALS_WRONG_CHAR) 

def calculate_closenessByNeighboring(correct_word, try_word):
    sumNeighborsPoints=len(correct_word) - len(try_word)
    min_len = min(len(correct_word), len(try_word))
      # Compare character by character up to the length of the shorter word
    for i in range(min_len):
       distance = get_keyboard_distance(correct_word[i], try_word[i])
       sumNeighborsPoints += distance
    return  calculate_point_For_Question(correct_word,sumNeighborsPoints)
   
def calculate_point_For_Question(correct_word,point_For_Word):
    return float((point_For_Word/(len(correct_word)*10)))

def calculate_closenessByLevenshtein(correct_word, try_word):
    distance = Levenshtein.distance(correct_word, try_word)
    max_len = max(len(correct_word), len(try_word))
    closeness = float(distance) if max_len == 0 else float(distance) / float(max_len)
    return float((10 - closeness) / 10)



class Question:
    def __init__(self, word: Word):
        self.word = word
        self.try_answer = ""
        self.levenshtein_distance = -1
        self.neighbors_distance = -1
        self.point = 0
        self.right = False
        
    def ask_question(self):
        self.init_try_answer()
        self.levenshtein_distance = calculate_closenessByLevenshtein(self.word.word, self.try_answer.strip())
        self.neighbors_distance = calculate_closenessByNeighboring(self.word.get_word(), self.try_answer)
        self.point = round((((self.levenshtein_distance / 3)) + ((2 * self.neighbors_distance / 3))) * 100, 1)
        if self.point == FINALS_CORRECT_WORD:
            self.right = True

    def init_try_answer(self):
        self.try_answer = input("Please enter your answer: ")

    def __str__(self):
        return (
            f"Word: {self.word.word}\n"
            f"  User Answer: {self.try_answer}\n"
            f"  Levenshtein Distance: {self.levenshtein_distance}\n"
            f"  Neighbor Distance: {self.neighbors_distance}\n"
            f"  Point: {round(self.point, 1)}\n"
            f"  Correct: {self.right}"
        )

    def __init__(self, word: Word):
        self.word = word
        self.try_answer = ""
        self.levenshtein_distance = -1  # Initially, set it to -1
        self.neighbors_distance = -1  # Initialize the neighbor distance
        self.point = 0
        self.right=False
        
    def ask_question(self):
        self.init_try_answer()
        """Prompts the user to enter an answer and checks how close it is."""
        self.levenshtein_distance = calculate_closenessByLevenshtein(self.word.word, self.try_answer.strip())  # Calculate the Levenshtein distance
        self.neighbors_distance = calculate_closenessByNeighboring(self.word.get_word(), self.try_answer)  # Calculate the neighbors distance (how many characters are typed with neighboring keys)
        self.point = round((((self.levenshtein_distance / 3)) + ((2 * self.neighbors_distance / 3))) * 100, 1)
        if self.point == FINALS_CORRECT_WORD:
            self.right = True  # Fixed assignment

      
    def init_try_answer(self):
        self.try_answer = input("Please enter your answer: ")
        
    def __str__(self):
        return (
            f"Word: {self.word.word}\n"
            f"  User Answer: {self.try_answer}\n"
          # f"  Levenshtein Distance: {self.levenshtein_distance}\n"
          # f"  Neighbor Distance: {self.neighbors_distance}\n"
            f"  Point: {round(self.point, 1)}\n"
            f"  Correct: {self.right}"
    )