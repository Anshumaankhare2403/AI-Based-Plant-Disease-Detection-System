"""
PlantCare AI - Disease Prediction Route
=======================================
"""

import base64
from flask import Blueprint, request, jsonify
from predictor import predictor
from firebase_service import persistence_service
from config import Config

predict_bp = Blueprint("predict_bp", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@predict_bp.route("/predict", methods=["POST"])
def predict():
    # 1. Check model availability
    if not predictor.is_loaded:
        predictor._load_model()
        if not predictor.is_loaded:
            return jsonify({
                "success": False,
                "error": "CNN model is currently unavailable. Ensure training is complete.",
                "details": predictor.load_error
            }), 503

    # 2. File presence validation
    file_field = None
    if "image" in request.files:
        file_field = request.files["image"]
    elif "file" in request.files:
        file_field = request.files["file"]

    if not file_field or file_field.filename == "":
        return jsonify({
            "success": False,
            "error": "No image file provided. Please upload an image with the field name 'image' or 'file'."
        }), 400

    filename = file_field.filename
    if not allowed_file(filename):
        return jsonify({
            "success": False,
            "error": f"Unsupported file type. Allowed formats: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        }), 400

    # 3. Read bytes and check size
    file_bytes = file_field.read()
    if len(file_bytes) == 0:
        return jsonify({
            "success": False,
            "error": "Uploaded file is empty."
        }), 400

    if len(file_bytes) > Config.MAX_CONTENT_LENGTH:
        return jsonify({
            "success": False,
            "error": f"Image exceeds maximum allowable size of {Config.MAX_CONTENT_LENGTH // (1024*1024)}MB."
        }), 413

    # 4. Run prediction
    pred_result = predictor.predict(file_bytes)
    if not pred_result.get("success"):
        return jsonify({
            "success": False,
            "error": pred_result.get("error", "Failed to process image.")
        }), 400

    # 5. Extract user_id if supplied in headers or form data
    user_id = request.headers.get("X-User-Id") or request.form.get("user_id") or "anonymous_guest"

    # 6. Encode image preview for history persistence
    img_mime = "image/jpeg" if filename.lower().endswith((".jpg", ".jpeg")) else "image/png"
    base64_str = f"data:{img_mime};base64,{base64.b64encode(file_bytes).decode('utf-8')}"

    # 7. Persist to Firestore or local SQLite
    record_to_save = {
        "user_id": user_id,
        "plant": pred_result["plant"],
        "disease": pred_result["disease"],
        "raw_class": pred_result["raw_class"],
        "confidence": pred_result["confidence"],
        "severity": pred_result["severity"],
        "status": pred_result["status"],
        "image_base64": base64_str,
        "recommendations": pred_result["recommendations"],
        "top_3": pred_result["top_3"]
    }
    pred_id = persistence_service.save_prediction(record_to_save)
    pred_result["id"] = pred_id

    return jsonify({
        "success": True,
        "data": pred_result
    }), 200

