"""
PlantCare AI - Health & Model Info Endpoints
============================================
"""

import time
import platform
from flask import Blueprint, jsonify
from predictor import predictor
from firebase_service import persistence_service
from config import Config

health_bp = Blueprint("health_bp", __name__)
START_TIME = time.time()


@health_bp.route("/health", methods=["GET"])
def health_check():
    uptime_seconds = round(time.time() - START_TIME, 1)
    status_data = persistence_service.get_status()
    model_info = predictor.get_model_info()

    return jsonify({
        "status": "healthy",
        "service": "PlantCare AI REST API",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "environment": Config.ENV,
        "platform": platform.platform(),
        "persistence": status_data,
        "model_status": model_info["status"]
    }), 200


@health_bp.route("/model/info", methods=["GET"])
def model_info():
    info = predictor.get_model_info()
    return jsonify({
        "success": True,
        "data": info
    }), 200

