from flask import Blueprint, request, jsonify, session
from functools import wraps

from app.models.user import User
from app import db
from app.utils.activity_logger import log_activity

auth_bp = Blueprint("auth", __name__, url_prefix="/api")



def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        if session.get("role") != "admin":
            return jsonify({"success": False, "message": "Forbidden"}), 403

        return f(*args, **kwargs)
    return wrapper


# ===============================
# LOGIN
# ===============================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    if not user.check_password(password):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    # ✅ LOGIN SUCCESS — ROLE COMES FROM DB
    session["user_id"] = user.id
    session["user_name"] = user.username
    session["role"] = user.role

    log_activity("Login", f"{user.username} logged in")

    return jsonify({
        "success": True,
          # optional, frontend already gets via check_session
    })

# ===============================
# CHECK SESSION (USED BY NAVBAR)
# ===============================
@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    if "user_id" not in session:
        return jsonify({"logged_in": False})

    return jsonify({
        "logged_in": True,
        "role": session.get("role")   # ✅ ADDED
    })


# ===============================
# LOGOUT
# ===============================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    log_activity("Logout", "Success")
    session.clear()
    return jsonify({"success": True})


# ===============================
# SIGNUP (ADMIN ONLY)
# ===============================
@auth_bp.route("/signup", methods=["POST"])
@admin_required
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify({
            "success": False,
            "message": "Username, password, and role are required"
        }), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({
            "success": False,
            "message": "Username already exists"
        }), 409

    user = User(username=username, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    log_activity("Signup", f"User {username} created")

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    }), 201


# ===============================
# LIST USERS (ADMIN ONLY)
# ===============================
@auth_bp.route("/signup", methods=["GET"])
@admin_required
def list_users():
    users = User.query.order_by(User.id).all()

    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "phone": u.phone
        }
        for u in users
    ])


# ===============================
# DELETE USER (ADMIN ONLY)
# ===============================
@auth_bp.route("/signup/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    log_activity("Delete User", f"User ID {user_id} deleted")

    return jsonify({"success": True})
