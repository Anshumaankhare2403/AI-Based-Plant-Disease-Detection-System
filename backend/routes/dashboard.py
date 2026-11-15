"""
PlantCare AI - Analytics & Dashboard Statistics Endpoint
========================================================
"""

from flask import Blueprint, request, jsonify
from firebase_service import persistence_service

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    user_id = request.headers.get("X-User-Id") or request.args.get("user_id")

    try:
        stats = persistence_service.get_stats(user_id=user_id)
        return jsonify({
            "success": True,
            "data": stats
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to retrieve dashboard stats: {str(e)}"
        }), 500

