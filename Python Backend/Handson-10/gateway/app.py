from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# ✅ FIX: correct port for course service
COURSE_SERVICE = "http://127.0.0.1:5000"
STUDENT_SERVICE = "http://127.0.0.1:5002"

# ---------------- COURSE ROUTES ----------------

@app.route("/api/courses", methods=["GET"])
def courses():
    try:
        response = requests.get(f"{COURSE_SERVICE}/api/courses")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Course Service is not running"}), 503


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def course_by_id(course_id):
    try:
        response = requests.get(f"{COURSE_SERVICE}/api/courses/{course_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Course Service is not running"}), 503


# ---------------- STUDENT ROUTES ----------------

@app.route("/api/students", methods=["GET"])
def get_students():
    try:
        response = requests.get(f"{STUDENT_SERVICE}/api/students")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Student Service is not running"}), 503


@app.route("/api/students", methods=["POST"])
def add_student():
    try:
        response = requests.post(
            f"{STUDENT_SERVICE}/api/students",
            json=request.json
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Student Service is not running"}), 503


if __name__ == "__main__":
    app.run(port=5001, debug=True)