"""
PlantCare AI - Model Evaluation & Diagnostics
=============================================
Computes:
1. Overall Accuracy, Loss on Actual Test Partition
2. Per-class Precision, Recall, and F1-Score (Pure NumPy - SAC Compliant)
3. Macro & Weighted Average Metrics
4. Confusion Matrix Visualization (Matplotlib Heatmap)
5. Comprehensive Evaluation Report Output (JSON & Markdown)
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if "KERAS_BACKEND" not in os.environ:
    os.environ["KERAS_BACKEND"] = "torch"

import keras

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
TEST_DIR = DATASET_DIR / "test"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR.parent / "docs"

IMG_HEIGHT = 128
IMG_WIDTH = 128


def compute_metrics(y_true, y_pred, class_names):
    """
    Pure NumPy implementation of Confusion Matrix, Precision, Recall, and F1.
    100% resilient across all operating system security policies.
    """
    n_classes = len(class_names)
    cm = np.zeros((n_classes, n_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1

    accuracy = float(np.mean(y_true == y_pred))
    
    cls_report = {}
    precisions = []
    recalls = []
    f1s = []
    supports = []

    for i, cls in enumerate(class_names):
        tp = cm[i, i]
        fp = np.sum(cm[:, i]) - tp
        fn = np.sum(cm[i, :]) - tp
        support = int(np.sum(cm[i, :]))

        p = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        r = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = float(2 * p * r / (p + r)) if (p + r) > 0 else 0.0

        precisions.append(p)
        recalls.append(r)
        f1s.append(f1)
        supports.append(support)

        cls_report[cls] = {
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f1-score": round(f1, 4),
            "support": support
        }

    total_samples = sum(supports)
    macro_p = float(np.mean(precisions))
    macro_r = float(np.mean(recalls))
    macro_f1 = float(np.mean(f1s))

    weighted_p = float(sum(p * s for p, s in zip(precisions, supports)) / total_samples) if total_samples > 0 else 0.0
    weighted_r = float(sum(r * s for r, s in zip(recalls, supports)) / total_samples) if total_samples > 0 else 0.0
    weighted_f1 = float(sum(f1 * s for f1, s in zip(f1s, supports)) / total_samples) if total_samples > 0 else 0.0

    cls_report["macro avg"] = {
        "precision": round(macro_p, 4),
        "recall": round(macro_r, 4),
        "f1-score": round(macro_f1, 4),
        "support": total_samples
    }
    cls_report["weighted avg"] = {
        "precision": round(weighted_p, 4),
        "recall": round(weighted_r, 4),
        "f1-score": round(weighted_f1, 4),
        "support": total_samples
    }

    return cm, accuracy, macro_p, macro_r, macro_f1, weighted_p, weighted_r, weighted_f1, cls_report


def load_test_arrays(class_names):
    images = []
    labels = []
    class_to_idx = {cls: idx for idx, cls in enumerate(class_names)}

    for cls in class_names:
        class_folder = TEST_DIR / cls
        if not class_folder.exists():
            continue
        idx = class_to_idx[cls]
        for img_file in class_folder.iterdir():
            if img_file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                try:
                    with Image.open(img_file) as img:
                        img_rgb = img.convert("RGB")
                        if img_rgb.size != (IMG_WIDTH, IMG_HEIGHT):
                            img_rgb = img_rgb.resize((IMG_WIDTH, IMG_HEIGHT))
                        images.append(np.array(img_rgb, dtype=np.float32))
                        labels.append(idx)
                except Exception as e:
                    print(f"Error reading {img_file}: {e}")

    X_test = np.array(images, dtype=np.float32)
    y_test = np.array(labels, dtype=np.int64)
    return X_test, y_test


def evaluate_model(model_path=None):
    if model_path is None:
        model_path = MODELS_DIR / "plant_disease_model_best.keras"
        if not model_path.exists():
            model_path = MODELS_DIR / "plant_disease_model_final.keras"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}. Please run train.py first.")

    with open(MODELS_DIR / "class_names.json", "r", encoding="utf-8") as f:
        class_names = json.load(f)

    print(f"[Evaluation] Loading model from {model_path}...")
    model = keras.models.load_model(str(model_path))
    
    X_test, y_true = load_test_arrays(class_names)
    print(f"[Evaluation] Predicting on actual test dataset ({len(X_test)} samples)...")
    
    y_pred_probs = model.predict(X_test, batch_size=32, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    cm, accuracy, macro_p, macro_r, macro_f1, weighted_p, weighted_r, weighted_f1, cls_report = compute_metrics(
        y_true, y_pred, class_names
    )

    # Plot Confusion Matrix with Matplotlib
    cm_path = MODELS_DIR / "confusion_matrix.png"
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Greens)
    plt.title("PlantCare AI - Confusion Matrix (Test Split)", fontsize=13, fontweight="bold")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    clean_labels = [c.replace("___", " ").replace("_", " ") for c in class_names]
    plt.xticks(tick_marks, clean_labels, rotation=45, ha="right", fontsize=9)
    plt.yticks(tick_marks, clean_labels, fontsize=9)

    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     ha="center", va="center",
                     color="white" if cm[i, j] > thresh else "black",
                     fontsize=9)

    plt.ylabel("True Class", fontsize=11)
    plt.xlabel("Predicted Class", fontsize=11)
    plt.tight_layout()
    plt.savefig(cm_path, dpi=200)
    plt.close()

    metrics = {
        "model_file": str(model_path.name),
        "test_samples": int(len(y_true)),
        "accuracy": accuracy,
        "precision_macro": macro_p,
        "recall_macro": macro_r,
        "f1_macro": macro_f1,
        "precision_weighted": weighted_p,
        "recall_weighted": weighted_r,
        "f1_weighted": weighted_f1,
        "classification_report": cls_report
    }

    # Save metrics JSON
    metrics_path = MODELS_DIR / "evaluation_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Save Evaluation Markdown Report
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    report_md_path = DOCS_DIR / "model-evaluation.md"
    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("# PlantCare AI - Comprehensive Model Evaluation Report\n\n")
        f.write(f"**Evaluated Model:** `{model_path.name}`  \n")
        f.write(f"**Test Set Samples:** {len(y_true)}  \n\n")
        f.write("## Overall Performance Summary\n\n")
        f.write(f"- **Accuracy:** {accuracy * 100:.2f}%\n")
        f.write(f"- **Macro Precision:** {macro_p:.4f}\n")
        f.write(f"- **Macro Recall:** {macro_r:.4f}\n")
        f.write(f"- **Macro F1-Score:** {macro_f1:.4f}\n")
        f.write(f"- **Weighted F1-Score:** {weighted_f1:.4f}\n\n")
        f.write("## Classification Report\n\n")
        f.write("| Class Name | Precision | Recall | F1-Score | Support |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: |\n")
        for cls_name, vals in cls_report.items():
            f.write(f"| `{cls_name}` | {vals['precision']} | {vals['recall']} | {vals['f1-score']} | {vals['support']} |\n")
        f.write(f"\n## Confusion Matrix Artifact\n\n")
        f.write(f"Saved to: `ml-model/models/{cm_path.name}`\n")

    print("\n" + "=" * 60)
    print("PLANTCARE AI - MODEL EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Overall Test Accuracy: {accuracy * 100:.2f}%")
    print(f"Macro F1-Score:       {macro_f1:.4f}")
    print(f"Weighted F1-Score:    {weighted_f1:.4f}")
    print(f"Metrics saved to:     {metrics_path}")
    print(f"Confusion Matrix:     {cm_path}")
    print(f"Report saved to:      {report_md_path}")
    print("=" * 60)

    return metrics


if __name__ == "__main__":
    evaluate_model()
