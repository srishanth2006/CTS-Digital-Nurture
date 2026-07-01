from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Course Management API"
    })

@app.route("/courses")
def get_courses():
    courses = [
        {
            "id": 1,
            "name": "Python Programming",
            "credits": 4
        },
        {
            "id": 2,
            "name": "Database Systems",
            "credits": 3
        }
    ]

    return jsonify(courses)

if __name__ == "__main__":
    app.run(debug=True)