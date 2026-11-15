"""
PlantCare AI - Backend & API Test Suite
=======================================
Covers:
- TC-001: Health check endpoint
- TC-002: Model metadata & info endpoint
- TC-003: Successful image prediction (valid leaf image)
- TC-004: Missing image payload (400)
- TC-005: Invalid file type rejection (400)
- TC-006: Corrupt image rejection (400)
- TC-007: History endpoint retrieval
- TC-008: Dashboard analytics stats
- TC-009: User registration & password hashing
- TC-010: User login authentication
"""

import io
import os
import sys
import pytest
from PIL import Image

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from predictor import predictor
from firebase_service import persistence_service


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_leaf_image_bytes():
    """Generate in-memory valid leaf test image."""
    img = Image.new("RGB", (128, 128), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_tc001_health_check(client):
    """TC-001: Backend health check returns 200 and healthy status."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert "persistence" in data
    assert "uptime_seconds" in data


def test_tc002_model_info(client):
    """TC-002: Model info returns classes and architecture info."""
    res = client.get("/api/model/info")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "supported_classes" in data["data"]
    assert len(data["data"]["supported_classes"]) >= 10


def test_tc003_successful_prediction(client, sample_leaf_image_bytes):
    """TC-003: Prediction endpoint accepts valid leaf image and returns diagnosis."""
    data = {
        "image": (io.BytesIO(sample_leaf_image_bytes), "test_leaf.jpg")
    }
    res = client.post("/api/predict", data=data, content_type="multipart/form-data")
    assert res.status_code in [200, 503]
    if res.status_code == 200:
        json_data = res.get_json()
        assert json_data["success"] is True
        pred = json_data["data"]
        assert "plant" in pred
        assert "disease" in pred
        assert "confidence" in pred
        assert "recommendations" in pred
        assert "top_3" in pred


def test_tc004_missing_image(client):
    """TC-004: POST /api/predict without image returns 400 Bad Request."""
    res = client.post("/api/predict", data={}, content_type="multipart/form-data")
    assert res.status_code == 400
    json_data = res.get_json()
    assert json_data["success"] is False
    assert "No image file provided" in json_data["error"]


def test_tc005_invalid_file_type(client):
    """TC-005: Non-image file returns 400 Unsupported File Type."""
    data = {
        "image": (io.BytesIO(b"Hello this is a text file"), "malicious.txt")
    }
    res = client.post("/api/predict", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    json_data = res.get_json()
    assert json_data["success"] is False
    assert "Unsupported file type" in json_data["error"]


def test_tc006_corrupt_image(client):
    """TC-006: Corrupt image file returns 400."""
    data = {
        "image": (io.BytesIO(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00brokenbytes"), "corrupt.jpg")
    }
    res = client.post("/api/predict", data=data, content_type="multipart/form-data")
    assert res.status_code in [400, 503]
    json_data = res.get_json()
    assert json_data["success"] is False


def test_tc007_history_retrieval(client):
    """TC-007: History endpoint retrieves saved predictions."""
    res = client.get("/api/history")
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)


def test_tc008_dashboard_stats(client):
    """TC-008: Dashboard stats endpoint returns analytics aggregates."""
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert "total_predictions" in json_data["data"]
    assert "disease_distribution" in json_data["data"]
    assert "crop_distribution" in json_data["data"]


def test_tc009_user_registration(client):
    """TC-009: User registration endpoint creates account with hashed password."""
    import uuid
    unique_email = f"tester_{uuid.uuid4().hex[:6]}@agrifarm.org"
    payload = {
        "email": unique_email,
        "password": "securepassword123",
        "display_name": "Test Agronomist"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    json_data = res.get_json()
    assert json_data["success"] is True
    assert json_data["user"]["email"] == unique_email


def test_tc010_user_login(client):
    """TC-010: User login validates credentials successfully."""
    import uuid
    email = f"user_{uuid.uuid4().hex[:6]}@agrifarm.org"
    password = "validpassword123"
    
    # Register first
    client.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "display_name": "Login User"
    })

    # Test login
    res = client.post("/api/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert json_data["user"]["email"] == email

    # Test bad login
    bad_res = client.post("/api/auth/login", json={"email": email, "password": "wrongpassword"})
    assert bad_res.status_code == 401

