import unittest

class TestWordLoader(unittest.TestCase):
    def test_load_20_words_from_file(self):
        file_path = r"C:\Users\User\OneDrive\שולחן העבודה\Work\פרויקט גמר\tamp\LexiLeap\rec\worlds\lesson3.txt"
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Tokenize words
        words = text.split()

        # Take the first 20 as strings
        first_20_words = words[:400]

        print("First 20 words:", first_20_words)

        # Optional: simple check
        self.assertEqual(len(first_20_words), 20)

if __name__ == '__main__':
    unittest.main()
