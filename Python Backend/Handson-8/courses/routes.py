from flask import Blueprint, jsonify, request
from extensions import db
from courses.models import Course

courses_bp = Blueprint("courses", __name__)

# Home
@courses_bp.route("/")
def home():
    return jsonify({"message": "Hands-On 7: Full CRUD API Running"})


# GET all courses
@courses_bp.route("/api/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "code": c.code,
            "credits": c.credits,
            "department": c.department.name
        }
        for c in courses
    ])


# GET course by ID
@courses_bp.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)

    return jsonify({
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits,
        "department": course.department.name
    })


# CREATE course
@courses_bp.route("/api/courses", methods=["POST"])
def create_course():
    data = request.get_json()

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data["department_id"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({"message": "Course created"}), 201


# UPDATE course
@courses_bp.route("/api/courses/<int:id>", methods=["PUT"])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()

    course.name = data.get("name", course.name)
    course.code = data.get("code", course.code)
    course.credits = data.get("credits", course.credits)
    course.department_id = data.get("department_id", course.department_id)

    db.session.commit()

    return jsonify({"message": "Course updated"})


# DELETE course
@courses_bp.route("/api/courses/<int:id>", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({"message": "Course deleted"})