"""
PlantCare AI - CNN Model Training Pipeline
==========================================
Builds and trains a Convolutional Neural Network for plant disease classification.
Uses Keras 3 with multi-backend execution (PyTorch/TensorFlow).
Architecture:
- Input (128x128x3)
- Rescaling (1./255)
- Data Augmentation (RandomFlip, RandomRotation)
- Conv2D (32, 3x3, padding='same') + ReLU + BatchNormalization + MaxPooling2D (2x2)
- Conv2D (64, 3x3, padding='same') + ReLU + BatchNormalization + MaxPooling2D (2x2)
- Conv2D (128, 3x3, padding='same') + ReLU + BatchNormalization + MaxPooling2D (2x2)
- GlobalAveragePooling2D
- Dense (128) + ReLU
- Dropout (0.35)
- Dense (num_classes) + Softmax
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if "KERAS_BACKEND" not in os.environ:
    os.environ["KERAS_BACKEND"] = "torch"

import keras
from keras import layers, regularizers

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "validation"
TEST_DIR = DATASET_DIR / "test"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

IMG_HEIGHT = 128
IMG_WIDTH = 128
CHANNELS = 3
BATCH_SIZE = 32
DEFAULT_EPOCHS = 12
RANDOM_SEED = 42


def load_class_names():
    class_file = MODELS_DIR / "class_names.json"
    if not class_file.exists():
        raise FileNotFoundError(f"Class names file not found at {class_file}. Run prepare_dataset.py first.")
    with open(class_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_split_arrays(split_dir, class_names):
    images = []
    labels = []
    class_to_idx = {cls: idx for idx, cls in enumerate(class_names)}

    for cls in class_names:
        class_folder = Path(split_dir) / cls
        if not class_folder.exists():
            continue
        idx = class_to_idx[cls]
        for img_file in class_folder.iterdir():
            if img_file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                try:
                    with Image.open(img_file) as img:
                        img_rgb = img.convert("RGB")
                        if img_rgb.size != (IMG_WIDTH, IMG_HEIGHT):
                            img_rgb = img_rgb.resize((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.BILINEAR)
                        images.append(np.array(img_rgb, dtype=np.float32))
                        labels.append(idx)
                except Exception as e:
                    print(f"Skipping damaged image {img_file}: {e}")

    X = np.array(images, dtype=np.float32)
    y = np.array(labels, dtype=np.int64)
    if len(X) > 0:
        rng = np.random.default_rng(RANDOM_SEED)
        indices = rng.permutation(len(X))
        X = X[indices]
        y = y[indices]
    return X, y


def load_datasets(batch_size=BATCH_SIZE):
    class_names = load_class_names()
    X_train, y_train = load_split_arrays(TRAIN_DIR, class_names)
    X_val, y_val = load_split_arrays(VAL_DIR, class_names)
    X_test, y_test = load_split_arrays(TEST_DIR, class_names)
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def build_cnn_model(num_classes, config="dropout", l1_val=0.0, l2_val=0.0, dropout_rate=0.35, learning_rate=1e-3):
    reg = None
    if config == "l1" or l1_val > 0.0:
        reg = regularizers.l1(l1_val or 1e-4)
    elif config == "l2" or l2_val > 0.0:
        reg = regularizers.l2(l2_val or 1e-4)

    drop = dropout_rate if (config in ["dropout", "full"] and dropout_rate > 0) else 0.0

    model = keras.Sequential([
        layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, CHANNELS)),
        
        # Rescaling pixel values to [0, 1]
        layers.Rescaling(1./255),
        
        # Data Augmentation (active during training)
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),

        # Conv Block 1
        layers.Conv2D(32, (3, 3), padding="same", activation="relu", kernel_regularizer=reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Conv Block 2
        layers.Conv2D(64, (3, 3), padding="same", activation="relu", kernel_regularizer=reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Conv Block 3
        layers.Conv2D(128, (3, 3), padding="same", activation="relu", kernel_regularizer=reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Feature aggregation
        layers.GlobalAveragePooling2D(),
        
        # Dense classification head
        layers.Dense(128, activation="relu", kernel_regularizer=reg),
        layers.Dropout(drop) if drop > 0 else layers.Identity(),
        layers.Dense(num_classes, activation="softmax")
    ], name=f"PlantCare_CNN_{config}")

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def plot_and_save_history(history, output_path):
    epochs_range = range(1, len(history.history["accuracy"]) + 1)
    
    plt.figure(figsize=(12, 5))
    
    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, history.history["accuracy"], label="Training Accuracy", color="#16a34a", lw=2)
    plt.plot(epochs_range, history.history["val_accuracy"], label="Validation Accuracy", color="#2563eb", lw=2)
    plt.title("Model Accuracy per Epoch", fontsize=12, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.6)
    
    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, history.history["loss"], label="Training Loss", color="#dc2626", lw=2)
    plt.plot(epochs_range, history.history["val_loss"], label="Validation Loss", color="#ea580c", lw=2)
    plt.title("Model Loss per Epoch", fontsize=12, fontweight="bold")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"[Training] Training curves saved to {output_path}")


def train(epochs=DEFAULT_EPOCHS, batch_size=BATCH_SIZE, config="dropout", lr=1e-3):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    class_names = load_class_names()
    num_classes = len(class_names)
    print(f"[Training] Preparing CNN model for {num_classes} classes...")
    
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_datasets(batch_size=batch_size)
    print(f"[Training] Dataset loaded into memory: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")
    
    model = build_cnn_model(num_classes=num_classes, config=config, dropout_rate=0.35, learning_rate=lr)
    model.summary()

    best_model_path = MODELS_DIR / "plant_disease_model_best.keras"
    final_model_path = MODELS_DIR / "plant_disease_model_final.keras"
    
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=str(best_model_path),
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    print(f"\n[Training] Commencing training: {epochs} epochs, batch size={batch_size}, lr={lr}...")
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        batch_size=batch_size,
        epochs=epochs,
        callbacks=callbacks
    )
    
    # Save final model
    model.save(str(final_model_path))
    print(f"[Training] Best model saved to: {best_model_path}")
    print(f"[Training] Final model saved to: {final_model_path}")
    
    # Save history
    hist_dict = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open(MODELS_DIR / "training_history.json", "w", encoding="utf-8") as f:
        json.dump(hist_dict, f, indent=2)
        
    plot_and_save_history(history, MODELS_DIR / "training_curves.png")
    
    # Test set evaluation
    test_results = model.evaluate(X_test, y_test, batch_size=batch_size, verbose=0)
    print(f"\n[Test Evaluation on Actual Test Split]")
    print(f"Test Loss: {test_results[0]:.4f}")
    print(f"Test Accuracy: {test_results[1] * 100:.2f}%")
    
    return model, hist_dict, test_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train PlantCare AI CNN Model")
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--config", type=str, default="dropout", choices=["basic", "l1", "l2", "dropout"], help="CNN regularization config")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    args = parser.parse_args()
    
    train(epochs=args.epochs, batch_size=args.batch_size, config=args.config, lr=args.lr)
