from flask import Flask, jsonify
from flask_cors import CORS
from api.Teacher_api import teacher_api  # ✅ You already imported this

#from src.api.lesson_api import getTestByNum_outside  # ✅ ADD THIS


#fdgdfg
app = Flask(__name__) # שנה את הנתיב בהתאם למיקום ה-static שלך
CORS(app)

@app.route("/hi")
def say_hi():
    return "hi"

# Register your blueprint AFTER app is created
app.register_blueprint(teacher_api, url_prefix="/api/teacher")

@app.route("/levels/get/<int:num>")
def get_level(num):
    str = ""
    for i in range(0,num):
        str +="a"
    return str


@app.route("/api/test/<int:test_num>")
def get_test_words(test_num):
    try:
        words = getTestByNum_outside(test_num)
        return jsonify(words)
    except IndexError:
        return jsonify({"error": "Test number out of range"}), 404

if __name__ == '__main__':
    ##ssl_context = ('certs/localhost+2.pem', 'certs/localhost+2-key.pem')
    app.run(host='127.0.0.1', port=5000, debug=True)


