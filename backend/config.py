"""
PlantCare AI - Backend Configuration
====================================
Loads environment variables and sets runtime parameters for Flask,
ML inference, database persistence, and Firebase integration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

# Load .env if present
load_dotenv(ROOT_DIR / ".env")

class Config:
    # Flask settings
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ["true", "1", "yes"]
    PORT = int(os.getenv("PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "plantcare-ai-super-secret-key-2026")
    
    # Upload limits
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE_MB", 10)) * 1024 * 1024  # 10 MB limit
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    
    # ML Model paths
    MODEL_PATH = Path(os.getenv("MODEL_PATH", ROOT_DIR / "ml-model" / "models" / "plant_disease_model_best.keras"))
    FALLBACK_MODEL_PATH = Path(ROOT_DIR / "ml-model" / "models" / "plant_disease_model_final.keras")
    CLASS_NAMES_PATH = Path(os.getenv("CLASS_NAMES_PATH", ROOT_DIR / "ml-model" / "models" / "class_names.json"))
    METRICS_PATH = Path(ROOT_DIR / "ml-model" / "models" / "evaluation_metrics.json")
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.60))
    
    # Database
    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "plantcare.db"))
    
    # Firebase settings
    FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", str(BASE_DIR / "serviceAccountKey.json"))
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")

