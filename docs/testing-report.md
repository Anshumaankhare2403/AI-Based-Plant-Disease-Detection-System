# PlantCare AI – Comprehensive QA & Testing Report

**System Name:** PlantCare AI – Intelligent Plant Disease Detection System  
**Author:** Senior Full-Stack & QA Engineering Team  
**Environment:** Windows x64, Python 3.11.9, Node.js v26.13.0, Pytest 9.2.0, Vitest 5.1.0  
**Date of Execution:** 2026-11-16  

---

## 1. Executive Summary

All critical testing suites across Backend API, Machine Learning Pipeline, and Frontend UI were designed, implemented, and executed on the local environment.

| Test Suite | Total Executed | Passed | Failed | Blocked | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Backend REST API (Pytest)** | 10 | 10 | 0 | 0 | **100%** |
| **Machine Learning Pipeline (Pytest)** | 6 | 6 | 0 | 0 | **100%** |
| **Frontend UI & Components (Vitest)** | 4 | 4 | 0 | 0 | **100%** |
| **TOTAL** | **20** | **20** | **0** | **0** | **100%** |

---

## 2. Test Execution Details

### A. Backend API Test Suite (`backend/tests/test_backend.py`)

#### TEST CASE: TC-001
- **Feature:** Backend health check (`GET /api/health`)
- **Description:** Verifies service uptime, environment diagnostics, and active persistence status.
- **Expected Result:** API responds with HTTP 200 and JSON containing `"status": "healthy"`.
- **Actual Result:** HTTP 200 returned with uptime, environment, and persistence status.
- **Status:** **PASS**

#### TEST CASE: TC-002
- **Feature:** Model metadata inquiry (`GET /api/model/info`)
- **Description:** Validates retrieval of model status, supported classes list, and confidence threshold.
- **Expected Result:** HTTP 200 with at least 10 classes and confidence threshold 0.60.
- **Actual Result:** HTTP 200 with 14 classes cataloged and framework runtime parameters.
- **Status:** **PASS**

#### TEST CASE: TC-003
- **Feature:** Foliar disease prediction (`POST /api/predict`)
- **Description:** Submits a valid 128x128 JPEG leaf image via `multipart/form-data`.
- **Expected Result:** HTTP 200 with classification payload (plant, disease, confidence, recommendations).
- **Actual Result:** HTTP 200 returned with diagnosis, confidence percentage, top 3 hypotheses, and IPM protocols.
- **Status:** **PASS**

#### TEST CASE: TC-004
- **Feature:** Missing payload validation (`POST /api/predict`)
- **Description:** Dispatches empty POST request without file data.
- **Expected Result:** HTTP 400 Bad Request with informative error description.
- **Actual Result:** HTTP 400 returned with `"No image file provided"`.
- **Status:** **PASS**

#### TEST CASE: TC-005
- **Feature:** File extension whitelist rejection (`POST /api/predict`)
- **Description:** Submits a non-image file (`malicious.txt`).
- **Expected Result:** HTTP 400 with `"Unsupported file type"`.
- **Actual Result:** HTTP 400 returned with error citing allowed extensions (`jpg, jpeg, png, webp`).
- **Status:** **PASS**

#### TEST CASE: TC-006
- **Feature:** Corrupt image file decoding defense (`POST /api/predict`)
- **Description:** Submits damaged binary image payload.
- **Expected Result:** HTTP 400 rejection via Pillow inspection.
- **Actual Result:** HTTP 400 returned with `"Invalid or corrupt image file"`.
- **Status:** **PASS**

#### TEST CASE: TC-007
- **Feature:** Historical records retrieval (`GET /api/history`)
- **Description:** Queries persisted prediction records.
- **Expected Result:** HTTP 200 with array of prediction history items.
- **Actual Result:** HTTP 200 returned with structured records from SQLite/Firestore.
- **Status:** **PASS**

#### TEST CASE: TC-008
- **Feature:** Dashboard analytics aggregates (`GET /api/dashboard/stats`)
- **Description:** Queries total predictions, healthy/diseased counts, and distribution lists.
- **Expected Result:** HTTP 200 with valid analytics payload.
- **Actual Result:** HTTP 200 with accurate category counts and frequency breakdown.
- **Status:** **PASS**

#### TEST CASE: TC-009
- **Feature:** User registration & password hashing (`POST /api/auth/register`)
- **Description:** Registers new user credentials with salted SHA-256 encryption.
- **Expected Result:** HTTP 201 Created and user record returned without password leak.
- **Actual Result:** HTTP 201 Created with sanitized user object.
- **Status:** **PASS**

#### TEST CASE: TC-010
- **Feature:** User login authentication (`POST /api/auth/login`)
- **Description:** Validates legitimate credentials and rejects invalid passwords.
- **Expected Result:** HTTP 200 for valid password; HTTP 401 for incorrect password.
- **Actual Result:** HTTP 200 and HTTP 401 correctly emitted.
- **Status:** **PASS**

---

### B. Machine Learning Test Suite (`ml-model/tests/test_ml.py`)

#### TEST CASE: TC-011
- **Feature:** Dataset directory partition structure
- **Description:** Asserts existence of `dataset/train`, `dataset/validation`, and `dataset/test`.
- **Expected Result:** All three directory trees exist and contain class subfolders.
- **Actual Result:** Verified all partition paths exist.
- **Status:** **PASS**

#### TEST CASE: TC-012
- **Feature:** Class names serialization integrity
- **Description:** Asserts `class_names.json` is formatted properly with at least 10 classes.
- **Expected Result:** List of 14 valid class strings loaded.
- **Actual Result:** Verified 14 categories including Tomato, Potato, Corn, Apple, and Grape classes.
- **Status:** **PASS**

#### TEST CASE: TC-013
- **Feature:** Image preprocessing and normalization
- **Description:** Tests RGB conversion, bicubic/bilinear 128x128 resampling, and float32 tensor conversion.
- **Expected Result:** Output tensor shape `(128, 128, 3)`.
- **Actual Result:** Resampling produces exact shape `(128, 128, 3)`.
- **Status:** **PASS**

#### TEST CASE: TC-014
- **Feature:** CNN architecture structural verification
- **Description:** Asserts CNN possesses Conv2D, BatchNormalization, MaxPooling, GlobalAveragePooling, Dense, and Dropout.
- **Expected Result:** Model builds with input shape `(None, 128, 128, 3)` and output shape `(None, 14)`.
- **Actual Result:** Verified layer topology and output dimension.
- **Status:** **PASS**

#### TEST CASE: TC-015
- **Feature:** Softmax probability distribution invariant
- **Description:** Injects random tensor and verifies predicted probabilities sum to 1.0.
- **Expected Result:** $\sum_{i=1}^{14} P(y_i) = 1.0 \pm 10^{-4}$ and all $P(y_i) \ge 0$.
- **Actual Result:** Sum equals 1.0000 across all classes.
- **Status:** **PASS**

#### TEST CASE: TC-016
- **Feature:** Deduplication hash integrity
- **Description:** Tests MD5 perceptual hashing to ensure distinct images produce unique 32-character hashes.
- **Expected Result:** Distinct byte streams yield non-colliding hashes.
- **Actual Result:** Verified hash uniqueness for data leakage prevention.
- **Status:** **PASS**

---

### C. Frontend UI Test Suite (`frontend/src/tests/App.test.jsx`)

#### TEST CASE: TC-017
- **Feature:** Landing page branding and hero CTA rendering
- **Description:** Asserts brand title and "Diagnose Leaf Now" link render.
- **Expected Result:** Brand elements and primary CTA present in DOM.
- **Actual Result:** Verified presence in DOM.
- **Status:** **PASS**

#### TEST CASE: TC-018
- **Feature:** Navigation bar links
- **Description:** Asserts Home, Dashboard, History, Model Info, and About links exist.
- **Expected Result:** All main navigation links rendered with valid href targets.
- **Actual Result:** All navigation links present.
- **Status:** **PASS**

#### TEST CASE: TC-019
- **Feature:** Supported crop tags display
- **Description:** Verifies Tomato, Potato, and Corn badges render on the homepage.
- **Expected Result:** Crop badges visible.
- **Actual Result:** Verified in rendered DOM.
- **Status:** **PASS**

#### TEST CASE: TC-020
- **Feature:** Workflow pipeline 3-step visualization
- **Description:** Asserts 3 steps (Upload, Extraction, Action Plan) render.
- **Expected Result:** Workflow cards present with numerical indicators.
- **Actual Result:** Verified in rendered DOM.
- **Status:** **PASS**

---

## 3. Bug Tracking & Resolutions Log

| Bug ID | Component | Description | Root Cause | Resolution | Status |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **BUG-001** | ML Runtime | `ImportError: DLL load failed while importing _pywrap_tensorflow_internal` | Windows 11 Smart App Control (SAC) blocks unsigned 1GB DLLs in user directories | Configured Keras 3 with multi-backend execution (`KERAS_BACKEND=torch`) which utilizes signed native runtimes | **FIXED** |
| **BUG-002** | Training | `keras.utils.image_dataset_from_directory` raised `ImportError: tensorflow required` | Keras 3 utility defaulted to `tf.data.Dataset` | Built custom, high-speed NumPy array partition loader (`load_split_arrays`) loading 45MB dataset directly into RAM | **FIXED** |
| **BUG-003** | CNN Topology | Dense layer after Flatten had 4.2M parameters causing gradient saturation | Dense(128) connected to unpooled Flatten(32,768) | Replaced with `GlobalAveragePooling2D()` reducing parameters to 112k and accelerating inference to &lt;20ms | **FIXED** |
| **BUG-004** | Training | Wildly oscillating loss and slow convergence | Images were appended class-by-class without cross-class batch shuffling | Added NumPy random permutation index shuffling to `load_split_arrays` | **FIXED** |
| **BUG-005** | Frontend Tests | Vitest threw `Found multiple elements with text /PlantCare/i` | Query used `getByText` when brand string appeared in Navbar, Hero, and Footer | Refactored queries to `getAllByText` and `getAllByRole` | **FIXED** |

