from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

students = []

# ✅ FIXED: Correct Course Service URL (port 5000)
COURSE_SERVICE = "http://127.0.0.1:5000/api/courses"

# ---------------- GET STUDENTS ----------------
@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(students)

# ---------------- ADD STUDENT ----------------
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()

    # FIX: ensure courses list exists
    if "courses" not in data:
        data["courses"] = []

    students.append(data)

    return jsonify({
        "message": "Student added successfully",
        "student": data
    }), 201

# ---------------- ENROLL STUDENT ----------------
@app.route("/api/students/<int:student_id>/enroll", methods=["POST"])
def enroll_student(student_id):
    data = request.get_json()
    course_id = data.get("course_id")

    # find student
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    try:
        # FIXED URL usage
        response = requests.get(f"{COURSE_SERVICE}/{course_id}")

        # invalid course check
        if response.status_code != 200:
            return jsonify({"error": "Invalid course"}), 400

    except requests.exceptions.RequestException:
        return jsonify({"error": "Course service unavailable"}), 503

    # avoid duplicate enrollment
    if course_id not in student["courses"]:
        student["courses"].append(course_id)

    return jsonify({
        "message": "Student enrolled successfully",
        "student": student
    }), 200

# ---------------- RUN SERVICE ----------------
if __name__ == "__main__":
    app.run(port=5002, debug=True)