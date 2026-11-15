"""
PlantCare AI - Dataset Downloader and Kaggle Setup Helper
========================================================
This script provides utilities and instructions to acquire the PlantVillage dataset
(https://www.kaggle.com/datasets/emmarex/plantdisease).

Dataset License: CC0 / Public Domain (PlantVillage, Hughes & Salathé, 2015).
"""

import os
import sys
import argparse
import urllib.request
import zipfile
import shutil

DATASET_URL = "https://www.kaggle.com/datasets/emmarex/plantdisease"
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "dataset", "raw")


def print_instructions():
    print("=" * 70)
    print("PlantCare AI - PlantVillage Dataset Download Instructions")
    print("=" * 70)
    print(f"Dataset URL: {DATASET_URL}")
    print("\nOption 1: Using Kaggle CLI (Recommended)")
    print("1. Install Kaggle CLI: pip install kaggle")
    print("2. Set up kaggle.json in ~/.kaggle/kaggle.json")
    print("3. Execute: kaggle datasets download -d emmarex/plantdisease -p ml-model/dataset/raw --unzip")
    print("\nOption 2: Manual Download")
    print("1. Visit https://www.kaggle.com/datasets/emmarex/plantdisease")
    print("2. Click 'Download' (approx. 800MB - 1.5GB)")
    print(f"3. Extract the downloaded archive into: {os.path.abspath(RAW_DATA_DIR)}")
    print("4. Each subfolder should represent a class, e.g., 'Tomato___Early_blight'")
    print("=" * 70)


def verify_raw_dataset(raw_dir=None):
    if raw_dir is None:
        raw_dir = RAW_DATA_DIR
    
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir, exist_ok=True)
        return False, []
    
    classes = [d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))]
    valid_classes = []
    total_images = 0
    
    for cls in classes:
        cls_path = os.path.join(raw_dir, cls)
        images = [f for f in os.listdir(cls_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if images:
            valid_classes.append((cls, len(images)))
            total_images += len(images)
            
    return bool(valid_classes), valid_classes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PlantVillage dataset download helper")
    parser.add_argument("--check", action="store_true", help="Check if raw dataset is installed")
    args = parser.parse_args()
    
    if args.check:
        found, classes = verify_raw_dataset()
        if found:
            print(f"Found {len(classes)} classes with {sum(c[1] for c in classes)} images in {RAW_DATA_DIR}")
        else:
            print(f"No valid dataset classes found in {RAW_DATA_DIR}")
            print_instructions()
    else:
        print_instructions()

