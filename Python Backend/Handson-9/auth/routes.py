from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Blueprint
auth_bp = Blueprint("auth", __name__)

# ------------------------
# REGISTER USER
# ------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "student")   # default role

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    user = User(username=username, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ------------------------
# LOGIN USER (GET JWT TOKEN)
# ------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity={
        "id": user.id,
        "role": user.role
    })

    return jsonify({
        "token": token,
        "message": "Login successful"
    })

# ------------------------
# PROTECTED ROUTE
# ------------------------
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    return jsonify({
        "message": f"Welcome user {user_id}"
    })
@auth_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin_only():
    user = get_jwt_identity()

    if user["role"] != "admin":
        return jsonify({"message": "Admins only"}), 403

    return jsonify({"message": "Welcome Admin"})
@auth_bp.route("/student", methods=["GET"])
@jwt_required()
def student_only():
    user = get_jwt_identity()

    return jsonify({
        "message": f"Welcome Student {user}"
    })