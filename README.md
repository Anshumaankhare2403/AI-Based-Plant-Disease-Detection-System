# PlantCare AI – Intelligent Plant Disease Detection System

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![React 19](https://img.shields.io/badge/React-19.3-61dafb.svg)](https://react.dev/)
[![Flask 3.1](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![Keras 3](https://img.shields.io/badge/Keras-3.15-red.svg)](https://keras.io/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end, full-stack agricultural pathology diagnostic platform powered by deep Convolutional Neural Networks (CNNs). PlantCare AI enables farmers and agronomists to upload plant foliage photographs, receive instantaneous disease classification, and obtain tailored Integrated Pest Management (IPM) agronomic recommendations.

---

## 🌟 Key Capabilities

- **Deep CNN Diagnosis:** Multi-layer Convolutional Neural Network with Batch Normalization, Global Average Pooling, and Dropout.
- **Dual Management Prescriptions:** Every disease report delivers both organic/biological management methods and licensed chemical fungicides.
- **Interactive Web Dashboard:** Real-time outbreak epidemiology charts powered by Recharts (disease distribution, crop category ratios, recent scans).
- **Flexible Dual Persistence:** Operates in zero-configuration local SQLite mode (`plantcare.db`) or cloud Google Firebase mode (Cloud Firestore, Storage, and Authentication).
- **Low-Confidence Safeguards:** Automated threshold gating flags ambiguous or non-leaf photos rather than producing false diagnoses.
- **Multi-Crop Support:** 14 categories across Tomato, Potato, Corn (Maize), Apple, and Grape foliage based on the PlantVillage benchmark.

---

## 🏗️ System Architecture

```
PlantCare-AI/
├── frontend/                     # React 19 + Vite 8 + Tailwind CSS SPA
│   ├── src/
│   │   ├── components/           # Navbar, Footer, Cards, Modals
│   │   ├── pages/                # Landing, Detect, Dashboard, History, ModelInfo, About, Auth
│   │   ├── layouts/              # MainLayout wrapper
│   │   ├── services/             # Axios API client (api.js)
│   │   ├── context/              # AuthContext (local & Firebase auth state)
│   │   └── tests/                # Vitest & React Testing Library test suite
│   ├── package.json
│   └── vite.config.js
│
├── backend/                      # Python Flask REST API
│   ├── app.py                    # Application factory & Blueprint registration
│   ├── config.py                 # Centralized configuration & environment loader
│   ├── predictor.py              # Single-instance CNN inference engine
│   ├── firebase_service.py       # Dual-mode persistence layer (SQLite / Firestore)
│   ├── routes/                   # Modular route blueprints (predict, health, history, dashboard, auth)
│   ├── services/                 # Agronomic disease knowledge base (disease_info.py)
│   ├── tests/                    # Pytest backend test suite
│   └── requirements.txt
│
├── ml-model/                     # Machine Learning Pipeline
│   ├── dataset/                  # Partitions: raw/, train/, validation/, test/
│   ├── models/                   # Best model (.keras), class_names.json, training_curves.png
│   ├── prepare_dataset.py        # Image validation, corrupt detection, deduplication, 70/15/15 split
│   ├── train.py                  # CNN architecture builder & training pipeline
│   ├── evaluate.py               # Confusion matrix generator & classification report
│   ├── optimize.py               # Regularization & hyperparameter benchmark script
│   ├── predict_test.py           # Standalone CLI inference tester
│   └── requirements.txt
│
├── docs/                         # Technical documentation
│   ├── architecture.md           # System design & component specification
│   ├── testing-report.md         # QA test execution matrix (TC-001 through TC-020)
│   ├── user-guide.md             # Installation, runbook, and demonstration guide
│   └── model-comparison.md       # Empirical benchmark comparison table
│
├── logs/                         # Execution logs
│   ├── development.log
│   ├── training.log
│   ├── testing.log
│   ├── errors.log
│   └── qa-report.log
│
├── firestore.rules               # Cloud Firestore security rules
├── .env.example                  # Environment configuration template
├── .gitignore                    # Version control exclusions
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 – 3.12 (Python 3.11 recommended)
- Node.js (v18+) and npm

### 2. Setup Backend & Virtual Environment

```bash
# Clone the repository
git clone <repository_url> PlantCare-AI
cd PlantCare-AI

# Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install -r ml-model/requirements.txt
```

### 3. Setup Frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Run Dataset Pipeline & Model Training

```bash
# 1. Prepare and split dataset (70% Train, 15% Validation, 15% Test)
python ml-model/prepare_dataset.py

# 2. Train the CNN model (automatically saves best weights and curves)
python ml-model/train.py --epochs 12 --batch-size 32

# 3. Evaluate on actual test split and generate confusion matrix
python ml-model/evaluate.py
```

### 5. Start Application Servers

**Terminal 1 (Backend API):**
```bash
python backend/app.py
# Server active on http://127.0.0.1:5000
```

**Terminal 2 (Frontend Client):**
```bash
cd frontend
npm run dev
# Vite dev server active on http://localhost:5173
```

Navigate to `http://localhost:5173` in your browser.

---

## 🧪 Testing & Quality Assurance

Run the automated test suites:

```bash
# Backend REST API tests (10 Test Cases)
pytest backend/tests/ -v

# Machine Learning pipeline tests (6 Test Cases)
pytest ml-model/tests/ -v

# Frontend UI & Component tests (4 Test Cases)
cd frontend
npm run test
```

All 20 test cases pass with a **100% success rate**. Refer to `docs/testing-report.md` for full test execution logs.

---

## 🌿 Supported Crop & Pathology Categories

| Crop | Condition / Disease | Pathogen | Severity |
| :--- | :--- | :--- | :--- |
| **Tomato** | Early Blight | *Alternaria solani* (Fungus) | Moderate |
| **Tomato** | Late Blight | *Phytophthora infestans* (Oomycete) | Severe |
| **Tomato** | Healthy Foliage | None | Normal |
| **Potato** | Early Blight | *Alternaria solani* (Fungus) | Moderate |
| **Potato** | Late Blight | *Phytophthora infestans* (Oomycete) | Critical |
| **Potato** | Healthy Foliage | None | Normal |
| **Corn** | Common Rust | *Puccinia sorghi* (Fungus) | Moderate |
| **Corn** | Northern Leaf Blight | *Exserohilum turcicum* (Fungus) | Severe |
| **Corn** | Healthy Foliage | None | Normal |
| **Apple** | Apple Scab | *Venturia inaequalis* (Fungus) | Moderate |
| **Apple** | Black Rot | *Botryosphaeria obtusa* (Fungus) | High |
| **Apple** | Healthy Foliage | None | Normal |
| **Grape** | Black Rot | *Guignardia bidwellii* (Fungus) | High |
| **Grape** | Healthy Foliage | None | Normal |

---

## 🛡️ License

This project is licensed under the MIT License - see the LICENSE file for details.
PlantVillage dataset is distributed under Creative Commons CC0 (Public Domain).
