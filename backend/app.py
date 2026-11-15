"""
PlantCare AI - Flask Application Factory & Entrypoint
=====================================================
Main REST API server for the PlantCare AI System.
Coordinates model prediction, authentication, history management, and analytics.
"""

import os
import sys
import logging
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from routes.health import health_bp
from routes.predict import predict_bp
from routes.history import history_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from predictor import predictor

# Setup logging
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "development.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("PlantCareAPI")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend clients
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprints under /api prefix
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(predict_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": str(error.description if hasattr(error, 'description') else error)
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Resource Not Found",
            "message": f"Endpoint '{request.path}' was not found on this server."
        }), 404

    @app.errorhandler(413)
    def file_too_large(error):
        return jsonify({
            "success": False,
            "error": "Payload Too Large",
            "message": f"Image file exceeds maximum limit of {Config.MAX_CONTENT_LENGTH // (1024*1024)}MB."
        }), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal Server Error: {error}")
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500

    @app.before_request
    def log_request_info():
        if not request.path.endswith("/health"):
            logger.info(f"{request.method} {request.path} from {request.remote_addr}")

    logger.info("PlantCare AI Application initialized successfully.")
    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting PlantCare AI API on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)

