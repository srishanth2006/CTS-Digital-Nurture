from flask import Flask, jsonify

app = Flask(__name__)

courses = [
    {"id": 1, "name": "Python"},
    {"id": 2, "name": "Flask"},
    {"id": 3, "name": "Microservices"}
]

@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course)

if __name__ == "__main__":
    app.run(port=5000, debug=True)