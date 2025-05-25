from pathlib import Path
import sys,pandas as pd
from src.backEnd.Word import Word  # adjust this import if needed!
from setuptools import setup, find_packages



setup(
    name='LexiLeap',
    version='0.1',
    packages=find_packages(),
)


# Add the project root (LexiLeap) to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.backEnd.Word import Word


def load_words_from_csv():
    # Build the path to the CSV (relative to this script)
    csv_file = Path(__file__).parent.parent.parent / '400-most-common-english-words-csv.csv'
    
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Get the list of word strings from the 'word' column
    words_list = df['word'].tolist()
    
    # Create a list of Word objects
    word_objects = [Word(word) for word in words_list]
    
    return word_objects



class Word:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Word('{self.text}')"

if __name__ == "__main__":
    words = load_words_from_csv()
    print(words[:10])  # print the first 10 Word objects to check
