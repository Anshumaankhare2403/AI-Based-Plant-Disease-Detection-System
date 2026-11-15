"""
PlantCare AI - Standalone Image Inference Tester
================================================
Tests model prediction directly from the command line against any leaf image.
Returns:
- Predicted class
- Confidence score (%)
- Formatted plant name & condition
- Latency (milliseconds)
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from PIL import Image
import numpy as np

if "KERAS_BACKEND" not in os.environ:
    os.environ["KERAS_BACKEND"] = "torch"

import keras

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
CLASS_NAMES_FILE = MODELS_DIR / "class_names.json"


def load_model_and_classes(model_path=None):
    if model_path is None:
        model_path = MODELS_DIR / "plant_disease_model_best.keras"
        if not model_path.exists():
            model_path = MODELS_DIR / "plant_disease_model_final.keras"
            
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}. Train the model first.")
        
    with open(CLASS_NAMES_FILE, "r", encoding="utf-8") as f:
        class_names = json.load(f)
        
    model = keras.models.load_model(str(model_path))
    return model, class_names


def predict_image(image_path, model=None, class_names=None):
    if model is None or class_names is None:
        model, class_names = load_model_and_classes()

    start_time = time.time()
    
    # Load and preprocess
    with Image.open(image_path) as img:
        img_rgb = img.convert("RGB")
        img_resized = img_rgb.resize((128, 128))
        img_arr = np.array(img_resized, dtype=np.float32)
        # Model's first Rescaling layer handles / 255.0
        input_tensor = np.expand_dims(img_arr, axis=0)

    # Predict
    preds = model.predict(input_tensor, verbose=0)[0]
    duration_ms = (time.time() - start_time) * 1000

    top_idx = int(np.argmax(preds))
    confidence = float(preds[top_idx])
    raw_class = class_names[top_idx]

    # Parse plant and condition
    if "___" in raw_class:
        plant, disease = raw_class.split("___", 1)
        disease_clean = disease.replace("_", " ")
    else:
        plant = "Plant"
        disease_clean = raw_class.replace("_", " ")

    top3_indices = np.argsort(preds)[::-1][:3]
    top3 = [
        {"class": class_names[idx], "confidence": round(float(preds[idx]) * 100, 2)}
        for idx in top3_indices
    ]

    result = {
        "image_path": str(image_path),
        "raw_class": raw_class,
        "plant": plant,
        "disease": disease_clean,
        "confidence_percent": round(confidence * 100, 2),
        "inference_latency_ms": round(duration_ms, 2),
        "top_3_predictions": top3
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PlantCare AI Image Predictor")
    parser.add_argument("image_path", type=str, nargs="?", help="Path to input leaf image")
    args = parser.parse_args()

    target_image = args.image_path
    if not target_image:
        # Pick any test image from dataset
        test_dir = BASE_DIR / "dataset" / "test"
        for sub in test_dir.iterdir():
            if sub.is_dir():
                for f in sub.iterdir():
                    if f.suffix.lower() in [".jpg", ".png"]:
                        target_image = str(f)
                        break
            if target_image:
                break

    if not target_image or not os.path.exists(target_image):
        print(f"No valid image provided or found to predict.")
        sys.exit(1)

    print(f"[Inference Test] Evaluating: {target_image}")
    res = predict_image(target_image)
    print(json.dumps(res, indent=2))

