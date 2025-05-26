from flask import Flask, send_from_directory
from flask_cors import CORS
import OpenSSL

#fdgdfg
app = Flask(__name__) # שנה את הנתיב בהתאם למיקום ה-static שלך
CORS(app)

@app.route("/")
def say_hi():
    return "hi"

@app.route("/levels/get/<int:num>")
def get_level(num):
    str = ""
    for i in range(0,num):
        str +="a"
    return str


if __name__ == '__main__':
    ssl_context = ('certs/localhost+2.pem', 'certs/localhost+2-key.pem')
    app.run(host='127.0.0.1', port=5000, ssl_context=ssl_context, debug=True)