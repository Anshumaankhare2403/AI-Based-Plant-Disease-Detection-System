# PlantCare AI – User & Deployment Guide

---

## 1. Quick Start Guide

### Prerequisites:
- Python 3.10, 3.11, or 3.12 (Recommended: Python 3.11)
- Node.js (v18+) and npm
- Git

### Installation Steps:

#### 1. Clone & Set Up Virtual Environment:
```bash
git clone <repository_url> PlantCare-AI
cd PlantCare-AI

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install Python backend & ML requirements
pip install -r backend/requirements.txt
pip install -r ml-model/requirements.txt
```

#### 2. Set Up Frontend:
```bash
cd frontend
npm install
cd ..
```

#### 3. Prepare Dataset & Train Model:
```bash
# Prepares 14 classes from dataset, validates, deduplicates, and splits (70/15/15)
python ml-model/prepare_dataset.py

# Trains the CNN model and saves best weights to ml-model/models/
python ml-model/train.py --epochs 12 --batch-size 32
```

---

## 2. Running the Application

### Option A: Run Full Stack Simultaneously

**Terminal 1 (Flask REST API Server):**
```bash
# Windows
.\.venv\Scripts\python.exe backend/app.py
# Runs on http://127.0.0.1:5000
```

**Terminal 2 (React Vite Frontend):**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

Open your browser at `http://localhost:5173` to interact with the full application!

---

## 3. Step-by-Step Demonstration Walkthrough

1. **Homepage (`/`):**
   - Review supported crops (Tomato, Potato, Corn, Apple, Grape).
   - Click **Diagnose Leaf Now**.

2. **Diagnose Leaf (`/detect`):**
   - Drag and drop any crop leaf image (e.g. from `ml-model/dataset/test/` or your camera).
   - Click **Run CNN Diagnosis**.
   - Review the predicted plant, disease, confidence score, and tailored agronomic management actions (organic vs chemical).

3. **Analytics Dashboard (`/dashboard`):**
   - Observe live outbreak distribution charts, healthy vs diseased ratios, and recent field scans.

4. **Audit History (`/history`):**
   - Search by crop or disease name, filter by status, and click **Details** to inspect saved diagnoses.

5. **Model Info (`/model-info`):**
   - View CNN layer architecture, tensor shapes, parameters, and the regularization comparison benchmark table.

---

## 4. Configuration & Firebase Integration

By default, PlantCare AI operates in **Zero-Config Local Mode** using SQLite (`backend/plantcare.db`).

To enable Google Firebase:
1. Obtain `serviceAccountKey.json` from the Firebase Console (Project Settings > Service Accounts).
2. Place the file at `backend/serviceAccountKey.json`.
3. Set `FIREBASE_STORAGE_BUCKET=your-app.appspot.com` in `.env`.
4. Deploy security rules:
   ```bash
   firebase deploy --only firestore:rules
   ```
The backend automatically detects the credentials and switches from SQLite to Cloud Firestore without code modification!

