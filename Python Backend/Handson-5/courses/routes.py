from flask import Blueprint, jsonify, request

from extensions import db
from courses.models import Course

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/")
def home():
    return jsonify({
        "message": "Flask SQLAlchemy API is running"
    })


@courses_bp.route("/api/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()

    result = []

    for course in courses:
        result.append({
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "credits": course.credits,
            "department": course.department.name
        })

    return jsonify(result)


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

    return jsonify({
        "message": "Course created successfully"
    }), 201
