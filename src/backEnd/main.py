from Word import Word
from Question import Question

def main():
    # Ask the user to input a word for the question
    word_input = input("Enter a word to be used in the question: ")
    # Create a Word object with the user's input
    word = Word(word=word_input)
    
    # Create a Question object with the Word object
    question = Question(word=word)
    
    # Ask the user to answer the question
    question.ask_question()
    print(question)


# Ensure the main function is only executed when the script is run directly
if __name__ == "__main__":
    main()
