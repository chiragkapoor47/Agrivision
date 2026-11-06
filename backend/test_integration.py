"""
TAH-015: End-to-End Integration Verification Suite
Tests all core APIs, computer vision inference, severity segmentation,
and database persistence.
"""
import os
import sys
import json
import pytest
from fastapi.testclient import TestClient

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.database import SessionLocal
from app.models.user import User

client = TestClient(app)

def test_system_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["supported_crops_count"] == 9
    print("[PASS] System Health Check")

def test_user_registration_and_login():
    import uuid
    unique_email = f"farmer_{uuid.uuid4().hex[:6]}@kisan.in"
    reg_payload = {
        "full_name": "Birinchi Bora",
        "email": unique_email,
        "password": "passcode123",
        "phone": "+91 94350 99887",
        "state": "Assam",
        "district": "Jorhat",
        "village": "Titabor",
        "farm_size_acres": 4.0,
        "preferred_language": "as",
        "primary_crops": "Rice, Tomato"
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 201, reg_res.text
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["full_name"] == "Birinchi Bora"
    token = reg_data["access_token"]

    # Login
    login_res = client.post("/api/auth/login", json={"email": unique_email, "password": "passcode123"})
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # Profile me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["district"] == "Jorhat"
    print("[PASS] User Registration, Login & Profile Retrieval")
    return token

def test_disease_prediction_and_severity():
    sample_img_path = os.path.join(os.path.dirname(__file__), "ml_pipeline", "sample_data", "tomato_early_blight.jpg")
    assert os.path.exists(sample_img_path), f"Sample leaf not found at {sample_img_path}"

    with open(sample_img_path, "rb") as f:
        files = {"file": ("tomato_leaf.jpg", f, "image/jpeg")}
        data = {
            "crop_hint": "Tomato",
            "state": "Assam",
            "district": "Kamrup",
            "language": "en"
        }
        res = client.post("/api/predict", files=files, data=data)

    assert res.status_code == 200, res.text
    result = res.json()
    assert "crop" in result
    assert "disease" in result
    assert "severity" in result
    assert result["severity"]["affected_area_percentage"] >= 0.0
    assert result["severity"]["level"] in ["Low", "Moderate", "Severe", "None / Healthy"]
    assert len(result["organic_treatment"]["remedies"]) > 0
    assert len(result["chemical_treatment"]["active_ingredients"]) > 0
    assert "overlay_url" in result["severity"]
    print(f"[PASS] Leaf AI Prediction: {result['crop']} - {result['disease']}, Severity: {result['severity']['level']} ({result['severity']['affected_area_percentage']}%)")
    return result["id"]

def test_healthy_leaf_prediction():
    sample_img_path = os.path.join(os.path.dirname(__file__), "ml_pipeline", "sample_data", "healthy_tomato_leaf.jpg")
    with open(sample_img_path, "rb") as f:
        files = {"file": ("healthy_leaf.jpg", f, "image/jpeg")}
        data = {"crop_hint": "Tomato", "state": "Punjab", "district": "Ludhiana"}
        res = client.post("/api/predict", files=files, data=data)

    assert res.status_code == 200
    result = res.json()
    assert "severity" in result
    print(f"[PASS] Healthy Leaf Evaluation: Severity={result['severity']['level']}")

def test_dashboard_statistics():
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["total_diagnoses"] > 0
    assert "severity_distribution" in data
    assert "crop_distribution" in data
    print(f"[PASS] Dashboard Statistics: Total Scans={data['total_diagnoses']}, Healthy={data['healthy_count']}, Infected={data['infected_count']}")

def test_diagnosis_history_and_deletion(diagnosis_id):
    # Fetch history
    history_res = client.get("/api/diagnosis/history")
    assert history_res.status_code == 200
    items = history_res.json()
    assert len(items) > 0

    # Fetch detail
    detail_res = client.get(f"/api/diagnosis/{diagnosis_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == diagnosis_id

    # Delete record
    del_res = client.delete(f"/api/diagnosis/{diagnosis_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] == True
    print(f"[PASS] History Listing, Detail Retrieval & Deletion of Record #{diagnosis_id}")

if __name__ == "__main__":
    print("\n--- Starting TAH-015 End-to-End Integration Tests ---\n")
    test_system_health()
    token = test_user_registration_and_login()
    diag_id = test_disease_prediction_and_severity()
    test_healthy_leaf_prediction()
    test_dashboard_statistics()
    test_diagnosis_history_and_deletion(diag_id)
    print("\n[ALL INTEGRATION TESTS PASSED SUCCESSFULLY!]\n")
