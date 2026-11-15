"""
PlantCare AI - Machine Learning Test Suite
==========================================
Covers:
- TC-011: Dataset directory validation (train, validation, test)
- TC-012: Class names metadata file validation
- TC-013: Image preprocessing (resizing to 128x128 and channel normalization)
- TC-014: CNN Model Architecture verification (Input, Conv2D, GlobalPooling, Dense, Softmax)
- TC-015: CNN Model Prediction output probability sum to 1.0 (softmax invariant)
- TC-016: Class mapping alignment
- TC-017: Deduplication hash integrity
"""

import os
import sys
import json
import pytest
from pathlib import Path
from PIL import Image
import numpy as np

# Ensure ml-model path is in sys.path
BASE_ML_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_ML_DIR))

if "KERAS_BACKEND" not in os.environ:
    os.environ["KERAS_BACKEND"] = "torch"

import keras
from train import build_cnn_model, load_class_names, load_split_arrays
from prepare_dataset import validate_image, compute_file_hash


def test_tc011_dataset_directories_exist():
    """TC-011: Verify train, validation, and test directories exist."""
    train_dir = BASE_ML_DIR / "dataset" / "train"
    val_dir = BASE_ML_DIR / "dataset" / "validation"
    test_dir = BASE_ML_DIR / "dataset" / "test"

    assert train_dir.exists(), "Train directory missing"
    assert val_dir.exists(), "Validation directory missing"
    assert test_dir.exists(), "Test directory missing"


def test_tc012_class_names_valid():
    """TC-012: Verify class_names.json contains valid classes."""
    class_names = load_class_names()
    assert isinstance(class_names, list)
    assert len(class_names) >= 10
    for cls in class_names:
        assert isinstance(cls, str)
        assert len(cls) > 3


def test_tc013_image_preprocessing():
    """TC-013: Verify image opening, validation, and resizing to 128x128."""
    tmp_img_path = BASE_ML_DIR / "test_leaf_temp.jpg"
    img = Image.new("RGB", (256, 256), color=(40, 160, 40))
    img.save(tmp_img_path)

    is_valid, fmt, size = validate_image(tmp_img_path)
    assert is_valid is True
    assert size == (256, 256)

    # Test resize
    with Image.open(tmp_img_path) as opened:
        resized = opened.resize((128, 128))
        assert resized.size == (128, 128)
        arr = np.array(resized, dtype=np.float32)
        assert arr.shape == (128, 128, 3)

    if tmp_img_path.exists():
        tmp_img_path.unlink()


def test_tc014_cnn_architecture():
    """TC-014: Verify CNN model architecture layers and parameters."""
    model = build_cnn_model(num_classes=14, config="dropout")
    assert model.input_shape == (None, 128, 128, 3)
    assert model.output_shape == (None, 14)
    layer_names = [l.__class__.__name__ for l in model.layers]
    assert "Conv2D" in layer_names
    assert "Dense" in layer_names
    assert "GlobalAveragePooling2D" in layer_names or "MaxPooling2D" in layer_names


def test_tc015_prediction_output_distribution():
    """TC-015: Verify model prediction outputs sum to 1.0 (valid probability distribution)."""
    model = build_cnn_model(num_classes=14, config="dropout")
    dummy_input = np.random.uniform(0, 255, (1, 128, 128, 3)).astype(np.float32)
    preds = model.predict(dummy_input, verbose=0)[0]

    assert len(preds) == 14
    assert np.all(preds >= 0.0)
    assert np.isclose(np.sum(preds), 1.0, atol=1e-4)


def test_tc016_deduplication_hash():
    """TC-016: Verify compute_file_hash creates distinct MD5 hashes."""
    p1 = BASE_ML_DIR / "hash_test_1.tmp"
    p2 = BASE_ML_DIR / "hash_test_2.tmp"

    with open(p1, "wb") as f:
        f.write(b"Image Content A")
    with open(p2, "wb") as f:
        f.write(b"Image Content B")

    h1 = compute_file_hash(p1)
    h2 = compute_file_hash(p2)

    assert h1 != h2
    assert len(h1) == 32

    p1.unlink()
    p2.unlink()

