"""
PlantCare AI - Authentication Route Handler
===========================================
Supports dual registration and login flows:
- Native local authentication with salted SHA-256 password hashing (SQLite mode)
- Firebase Auth integration when configured
"""

from flask import Blueprint, request, jsonify
from firebase_service import persistence_service

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    display_name = data.get("display_name", "").strip() or email.split("@")[0]

    if not email or "@" not in email:
        return jsonify({"success": False, "error": "A valid email address is required."}), 400

    if not password or len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters long."}), 400

    success, msg, user_data = persistence_service.register_user(email, password, display_name)
    if not success:
        return jsonify({"success": False, "error": msg}), 400

    return jsonify({
        "success": True,
        "message": msg,
        "user": user_data
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required."}), 400

    success, msg, user_data = persistence_service.authenticate_user(email, password)
    if not success:
        return jsonify({"success": False, "error": msg}), 401

    return jsonify({
        "success": True,
        "message": msg,
        "user": user_data
    }), 200


@auth_bp.route("/auth/status", methods=["GET"])
def auth_status():
    status = persistence_service.get_status()
    return jsonify({
        "success": True,
        "data": status
    }), 200

