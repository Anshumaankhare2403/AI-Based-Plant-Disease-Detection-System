"""
PlantCare AI - CNN Predictor Engine
===================================
Loads the trained CNN model once at application startup.
Performs image validation, preprocessing, model inference,
confidence assessment, and enriches predictions with agronomic recommendations.
"""

import os
import sys
import io
import time
import json
from pathlib import Path
from PIL import Image
import numpy as np

# Ensure backend consistency
if "KERAS_BACKEND" not in os.environ:
    os.environ["KERAS_BACKEND"] = "torch"

import keras
from config import Config
from services.disease_info import get_disease_details


class PlantCarePredictor:
    def __init__(self):
        self.model = None
        self.class_names = []
        self.is_loaded = False
        self.load_error = None
        self._load_model()

    def _load_model(self):
        try:
            # 1. Load class names
            class_path = Config.CLASS_NAMES_PATH
            if not class_path.exists():
                self.load_error = f"Class names file missing at {class_path}"
                print(f"[PlantCarePredictor] {self.load_error}")
                return

            with open(class_path, "r", encoding="utf-8") as f:
                self.class_names = json.load(f)

            # 2. Find model file (best or fallback)
            model_target = Config.MODEL_PATH
            if not model_target.exists():
                model_target = Config.FALLBACK_MODEL_PATH

            if not model_target.exists():
                self.load_error = f"Model file not found at {model_target}"
                print(f"[PlantCarePredictor] {self.load_error}")
                return

            print(f"[PlantCarePredictor] Loading CNN model from: {model_target}...")
            self.model = keras.models.load_model(str(model_target))
            self.is_loaded = True
            self.load_error = None
            print(f"[PlantCarePredictor] Successfully loaded model for {len(self.class_names)} classes.")
        except Exception as e:
            self.load_error = str(e)
            self.is_loaded = False
            print(f"[PlantCarePredictor] Model initialization failed: {e}")

    def get_model_info(self):
        metrics = {}
        if Config.METRICS_PATH.exists():
            try:
                with open(Config.METRICS_PATH, "r", encoding="utf-8") as f:
                    metrics = json.load(f)
            except Exception:
                pass

        return {
            "status": "ready" if self.is_loaded else "unavailable",
            "model_loaded": self.is_loaded,
            "classes_count": len(self.class_names),
            "supported_classes": self.class_names,
            "confidence_threshold": Config.CONFIDENCE_THRESHOLD,
            "target_resolution": "128x128",
            "framework": "Keras 3 / PyTorch Engine",
            "error": self.load_error,
            "evaluation_metrics": metrics
        }

    def predict(self, image_bytes: bytes):
        if not self.is_loaded:
            # Try reloading once in case training just completed
            self._load_model()
            if not self.is_loaded:
                return {
                    "success": False,
                    "error": f"Model is currently unavailable: {self.load_error}"
                }

        start_time = time.time()

        # 1. Image validation & decoding
        try:
            with Image.open(io.BytesIO(image_bytes)) as raw_img:
                raw_img.verify()
            
            # Reopen after verify
            with Image.open(io.BytesIO(image_bytes)) as img:
                img_format = img.format
                orig_size = img.size
                img_rgb = img.convert("RGB")
                img_resized = img_rgb.resize((128, 128), Image.Resampling.BILINEAR)
                img_array = np.array(img_resized, dtype=np.float32)
        except Exception as e:
            return {
                "success": False,
                "error": f"Invalid or corrupt image file: {str(e)}"
            }

        # 2. Batch expansion and inference
        input_tensor = np.expand_dims(img_array, axis=0)
        
        try:
            preds = self.model.predict(input_tensor, verbose=0)[0]
        except Exception as e:
            return {
                "success": False,
                "error": f"Inference execution failed: {str(e)}"
            }

        duration_ms = (time.time() - start_time) * 1000

        top_idx = int(np.argmax(preds))
        confidence = float(preds[top_idx])
        raw_class = self.class_names[top_idx]

        # Top 3 alternative predictions
        top3_indices = np.argsort(preds)[::-1][:3]
        top3 = [
            {
                "class": self.class_names[idx],
                "confidence": round(float(preds[idx]) * 100, 2),
                "plant": self.class_names[idx].split("___")[0] if "___" in self.class_names[idx] else "Plant",
                "disease": self.class_names[idx].split("___")[1].replace("_", " ") if "___" in self.class_names[idx] else self.class_names[idx]
            }
            for idx in top3_indices
        ]

        # 3. Confidence gating & Leaf verification
        is_confident = confidence >= Config.CONFIDENCE_THRESHOLD
        
        # Agronomic pathology details
        details = get_disease_details(raw_class)

        response = {
            "success": True,
            "raw_class": raw_class,
            "plant": details["plant"],
            "disease": details["disease"],
            "status": details["status"],
            "severity": details["severity"],
            "pathogen": details["pathogen"],
            "confidence": round(confidence * 100, 2),
            "confidence_ratio": float(confidence),
            "is_confident": is_confident,
            "confidence_warning": None if is_confident else (
                f"Prediction confidence ({confidence*100:.1f}%) is below the {Config.CONFIDENCE_THRESHOLD*100:.0f}% threshold. "
                "Ensure the photo shows a clear, well-lit crop leaf against a neutral background."
            ),
            "description": details["description"],
            "symptoms": details["symptoms"],
            "recommendations": {
                "organic_treatment": details["organic_treatment"],
                "chemical_treatment": details["chemical_treatment"],
                "prevention": details["prevention"]
            },
            "top_3": top3,
            "meta": {
                "latency_ms": round(duration_ms, 2),
                "original_dimensions": f"{orig_size[0]}x{orig_size[1]}",
                "processed_dimensions": "128x128",
                "format": img_format
            }
        }
        return response

# Global single instance
predictor = PlantCarePredictor()

