from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../static') # שנה את הנתיב בהתאם למיקום ה-static שלך
CORS(app)

@app.route('/', methods=['GET'])
def say_hi():
    return "hi"

@app.route('/test_page') # מסלול חדש לקובץ ה-HTML
def serve_test_page():
    return send_from_directory(app.static_folder, 'simple_test.html')

if __name__ == '__main__':
    app.run(port=5000)