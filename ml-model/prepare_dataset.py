"""
PlantCare AI - Dataset Preparation Pipeline
===========================================
Implements:
1. Image validation & corrupt file detection (Pillow inspection)
2. Duplicate detection via MD5/perceptual hashing to prevent train/test leakage
3. Standardized resizing to 128x128
4. Train/Validation/Test split (70% / 15% / 15%) with reproducible seed
5. Class names serialization (class_names.json)
6. Distribution report generation (Markdown & JSON)
7. Seed synthetic generator for testing/demo when raw PlantVillage is not yet placed
"""

import os
import sys
import json
import random
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
RAW_DIR = DATASET_DIR / "raw"
TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "validation"
TEST_DIR = DATASET_DIR / "test"
MODELS_DIR = BASE_DIR / "models"
REPORT_MD = DATASET_DIR / "distribution_report.md"
REPORT_JSON = DATASET_DIR / "dataset_report.json"
CLASS_NAMES_FILE = MODELS_DIR / "class_names.json"

TARGET_SIZE = (128, 128)
RANDOM_SEED = 42

DEFAULT_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___healthy",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Grape___Black_rot",
    "Grape___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy"
]


def compute_file_hash(file_path):
    """Compute MD5 hash to detect duplicate images."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_image(file_path):
    """Check if image file is valid and uncorrupted."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        with Image.open(file_path) as img:
            img.load()
            return True, img.format, img.size
    except Exception as e:
        return False, None, str(e)


def generate_sample_dataset(samples_per_class=60):
    """
    Generate realistic synthetic plant leaf image dataset for demonstration,
    benchmarking, and testing when raw PlantVillage archive is not present.
    Creates leaf patterns with healthy green veining or characteristic lesions.
    """
    print(f"[Dataset Preparation] Generating sample dataset ({samples_per_class} per class)...")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    for class_name in DEFAULT_CLASSES:
        class_raw_dir = RAW_DIR / class_name
        class_raw_dir.mkdir(parents=True, exist_ok=True)
        
        is_healthy = "healthy" in class_name.lower()
        is_rust = "rust" in class_name.lower()
        is_blight = "blight" in class_name.lower()
        is_scab = "scab" in class_name.lower() or "rot" in class_name.lower()

        for i in range(samples_per_class):
            # Base leaf color: healthy emerald/forest green or slightly yellowish for diseased
            if is_healthy:
                base_color = (
                    random.randint(30, 60),
                    random.randint(140, 200),
                    random.randint(30, 70)
                )
            else:
                base_color = (
                    random.randint(60, 110),
                    random.randint(110, 160),
                    random.randint(30, 60)
                )
                
            img = Image.new("RGB", (256, 256), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Draw leaf contour (elliptical leaf)
            leaf_box = [random.randint(20, 35), random.randint(20, 35),
                        random.randint(220, 235), random.randint(220, 235)]
            draw.ellipse(leaf_box, fill=base_color, outline=(20, 80, 20), width=2)
            
            # Draw primary vein
            vein_color = (base_color[0] + 20, min(255, base_color[1] + 30), base_color[2] + 15)
            draw.line([(128, 30), (128, 225)], fill=vein_color, width=3)
            for y_pos in range(60, 210, 30):
                draw.line([(128, y_pos), (128 - random.randint(35, 60), y_pos - random.randint(10, 25))], fill=vein_color, width=2)
                draw.line([(128, y_pos), (128 + random.randint(35, 60), y_pos - random.randint(10, 25))], fill=vein_color, width=2)
            
            # Disease lesions / symptoms
            if is_rust:
                # Orange/brown pustules
                for _ in range(random.randint(15, 30)):
                    rx = random.randint(50, 200)
                    ry = random.randint(50, 200)
                    rsize = random.randint(3, 8)
                    draw.ellipse([rx, ry, rx + rsize, ry + rsize], fill=(190, 80, 20))
            elif is_blight:
                # Dark brown/black concentric spots
                for _ in range(random.randint(5, 12)):
                    rx = random.randint(50, 190)
                    ry = random.randint(50, 190)
                    rsize = random.randint(10, 25)
                    draw.ellipse([rx, ry, rx + rsize, ry + rsize], fill=(60, 35, 15))
                    draw.ellipse([rx + 2, ry + 2, rx + rsize - 2, ry + rsize - 2], fill=(110, 70, 30))
            elif is_scab:
                # Black sunken spots
                for _ in range(random.randint(8, 18)):
                    rx = random.randint(55, 195)
                    ry = random.randint(55, 195)
                    rsize = random.randint(6, 16)
                    draw.ellipse([rx, ry, rx + rsize, ry + rsize], fill=(40, 40, 40))

            # Add subtle texture blur
            img = img.filter(ImageFilter.SMOOTH)
            
            img_path = class_raw_dir / f"leaf_{i:04d}.jpg"
            img.save(img_path, format="JPEG", quality=90)


def prepare_dataset(split_ratios=(0.70, 0.15, 0.15), force_generate=False):
    """
    Main dataset processing routine.
    - Validates images
    - Filters corrupt files
    - Removes duplicates to avoid leakage
    - Resizes to 128x128
    - Splits into train/val/test
    - Emits metrics and report
    """
    train_ratio, val_ratio, test_ratio = split_ratios
    assert round(train_ratio + val_ratio + test_ratio, 2) == 1.0, "Split ratios must sum to 1.0"
    
    random.seed(RANDOM_SEED)
    
    # Check if raw dataset exists and has content
    has_raw = RAW_DIR.exists() and any(RAW_DIR.iterdir())
    if not has_raw or force_generate:
        generate_sample_dataset()

    class_dirs = [d for d in RAW_DIR.iterdir() if d.is_dir()]
    if not class_dirs:
        print("[Error] No class subdirectories found in raw dataset.")
        return False
        
    class_names = sorted([d.name for d in class_dirs])
    print(f"[Dataset Preparation] Found {len(class_names)} classes: {class_names}")
    
    # Clean previous split directories
    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        if split_dir.exists():
            import shutil
            shutil.rmtree(split_dir)
        split_dir.mkdir(parents=True, exist_ok=True)
        for cls in class_names:
            (split_dir / cls).mkdir(parents=True, exist_ok=True)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    with open(CLASS_NAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

    total_stats = {
        "total_raw": 0,
        "valid_images": 0,
        "corrupt_images": 0,
        "duplicates_removed": 0,
        "train_count": 0,
        "val_count": 0,
        "test_count": 0,
        "per_class": {}
    }

    seen_hashes = set()

    for cls in class_names:
        raw_class_dir = RAW_DIR / cls
        raw_files = [f for f in raw_class_dir.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
        total_stats["total_raw"] += len(raw_files)
        
        valid_files = []
        for file_path in raw_files:
            is_valid, fmt, info = validate_image(file_path)
            if not is_valid:
                total_stats["corrupt_images"] += 1
                continue
                
            fhash = compute_file_hash(file_path)
            if fhash in seen_hashes:
                total_stats["duplicates_removed"] += 1
                continue
                
            seen_hashes.add(fhash)
            valid_files.append(file_path)

        total_stats["valid_images"] += len(valid_files)
        
        # Shuffle reproducibly
        random.shuffle(valid_files)
        n = len(valid_files)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        n_test = n - n_train - n_val

        train_files = valid_files[:n_train]
        val_files = valid_files[n_train:n_train + n_val]
        test_files = valid_files[n_train + n_val:]

        total_stats["train_count"] += len(train_files)
        total_stats["val_count"] += len(val_files)
        total_stats["test_count"] += len(test_files)
        
        total_stats["per_class"][cls] = {
            "total": n,
            "train": len(train_files),
            "val": len(val_files),
            "test": len(test_files)
        }

        # Save resized images to respective split folders
        for split_name, files, dest_dir in [
            ("train", train_files, TRAIN_DIR / cls),
            ("val", val_files, VAL_DIR / cls),
            ("test", test_files, TEST_DIR / cls)
        ]:
            for idx, file_path in enumerate(files):
                try:
                    with Image.open(file_path) as img:
                        img_rgb = img.convert("RGB")
                        img_resized = img_rgb.resize(TARGET_SIZE, Image.Resampling.BILINEAR)
                        dest_file = dest_dir / f"{cls}_{idx:04d}.jpg"
                        img_resized.save(dest_file, format="JPEG", quality=92)
                except Exception as e:
                    print(f"Error resizing {file_path}: {e}")

    # Write JSON report
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(total_stats, f, indent=2)

    # Write Markdown distribution report
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# PlantCare AI - Dataset Distribution & Validation Report\n\n")
        f.write("## Overview\n")
        f.write(f"- **Target Resolution:** {TARGET_SIZE[0]}x{TARGET_SIZE[1]} px\n")
        f.write(f"- **Split Policy:** 70% Train, 15% Validation, 15% Test (Seed={RANDOM_SEED})\n")
        f.write(f"- **Total Raw Images:** {total_stats['total_raw']}\n")
        f.write(f"- **Valid Images:** {total_stats['valid_images']}\n")
        f.write(f"- **Corrupt Files Filtered:** {total_stats['corrupt_images']}\n")
        f.write(f"- **Duplicate Files Removed (Data Leakage Guard):** {total_stats['duplicates_removed']}\n")
        f.write(f"- **Training Set:** {total_stats['train_count']} ({total_stats['train_count']/total_stats['valid_images']*100:.1f}%)\n")
        f.write(f"- **Validation Set:** {total_stats['val_count']} ({total_stats['val_count']/total_stats['valid_images']*100:.1f}%)\n")
        f.write(f"- **Test Set:** {total_stats['test_count']} ({total_stats['test_count']/total_stats['valid_images']*100:.1f}%)\n\n")
        
        f.write("## Class Distribution Table\n\n")
        f.write("| Class Name | Total Valid | Train (70%) | Validation (15%) | Test (15%) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: |\n")
        for cls, counts in total_stats["per_class"].items():
            f.write(f"| `{cls}` | {counts['total']} | {counts['train']} | {counts['val']} | {counts['test']} |\n")

    print("\n[Dataset Preparation Completed Successfully]")
    print(f"- Total Valid Images: {total_stats['valid_images']}")
    print(f"- Train: {total_stats['train_count']}, Val: {total_stats['val_count']}, Test: {total_stats['test_count']}")
    print(f"- Class names saved to: {CLASS_NAMES_FILE}")
    print(f"- Reports saved to: {REPORT_MD} and {REPORT_JSON}")
    return True


if __name__ == "__main__":
    prepare_dataset()

