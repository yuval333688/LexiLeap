def get_first_20_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = text.split()
    return words[:400]

if __name__ == "__main__":
    file_path = r"C:\Users\User\OneDrive\שולחן העבודה\Work\פרויקט גמר\tamp\LexiLeap\rec\worlds\lesson3.txt"
    first_20_words = get_first_20_words_from_file(file_path)
    print("First 20 words from file:")
    print(first_20_words)
