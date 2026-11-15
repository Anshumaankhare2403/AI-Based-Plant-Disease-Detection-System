"""
PlantCare AI - Detection History Endpoint
=========================================
"""

from flask import Blueprint, request, jsonify
from firebase_service import persistence_service

history_bp = Blueprint("history_bp", __name__)


@history_bp.route("/history", methods=["GET"])
def get_history():
    user_id = request.headers.get("X-User-Id") or request.args.get("user_id")
    limit = int(request.args.get("limit", 50))

    try:
        records = persistence_service.get_history(user_id=user_id, limit=limit)
        return jsonify({
            "success": True,
            "count": len(records),
            "data": records
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to retrieve history: {str(e)}"
        }), 500

