from flask import Flask, jsonify
from flask_cors import CORS   
from DatabaseManager import DatabaseManager
from lessons_fs import LessonsFS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
DatabaseManager.init()

@app.route("/get_levels")
def get_levels():
    return jsonify(DatabaseManager.get_lessons())


@app.route("/get_level/<int:num>")
def get_level(num: int):
    payload = LessonsFS.read_lesson(num)
    return jsonify(payload)

@app.route("/save_lesson/<int:id>/<int:score>")
def save_lesson(id:int, score:int ):
    return jsonify(DatabaseManager.update_lesson(id +1  , score))
                   






if __name__ == "__main__":
    app.run(debug=True)
