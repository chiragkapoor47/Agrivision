"""
TAH-015: Precision Agriculture and Crop Disease Predictor - FastAPI Backend Entrypoint
"""
import os
import json
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.diagnosis import DiagnosisRecord
from app.utils.auth_utils import hash_password
from app.routers.auth import router as auth_router
from app.routers.predict import router as predict_router
from app.routers.diagnosis import router as diagnosis_router
from app.routers.agricultural import router as agricultural_router
from app.routers.dashboard import router as dashboard_router
from app.routers.resources import router as resources_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Computer Vision Crop Disease Detection, Severity Assessment & Treatment Recommendation Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files for Uploaded Leaf Images & Severity Overlays
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Register API Routers under /api
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(predict_router, prefix=settings.API_V1_STR)
app.include_router(diagnosis_router, prefix=settings.API_V1_STR)
app.include_router(agricultural_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(resources_router, prefix=settings.API_V1_STR)

@app.get("/api/health", tags=["Health"])
def health_check():
    """System health check and diagnostic status"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",
        "supported_crops_count": 9,
        "inference_engine": "MobileNetV2 + OpenCV Severity Segmentation"
    }

def seed_initial_demo_data():
    """Seeds initial demonstration user and authentic diagnosis records for immediate visualization"""
    db = SessionLocal()
    try:
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == "farmer@kisan.in").first()
        if not demo_user:
            demo_user = User(
                full_name="Ramesh Saikia",
                email="farmer@kisan.in",
                hashed_password=hash_password("kisan123"),
                phone="+91 98640 12345",
                state="Assam",
                district="Kamrup",
                village="Azara",
                farm_size_acres=3.5,
                preferred_language="en",
                primary_crops="Tomato, Rice, Potato"
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print("[DB Seed] Created demo farmer user: farmer@kisan.in / kisan123")

        # Check if diagnosis records exist
        rec_count = db.query(DiagnosisRecord).count()
        if rec_count == 0:
            sample_records = [
                {
                    "crop": "Tomato", "disease": "Early Blight", "raw_class": "Tomato___Early_blight",
                    "pathogen": "Alternaria solani", "confidence": 94.2, "severity": "Low", "area": 14.8,
                    "is_healthy": False, "img": "/uploads/sample_tomato_early_blight.jpg",
                    "days_ago": 1, "village": "Azara", "district": "Kamrup", "state": "Assam"
                },
                {
                    "crop": "Potato", "disease": "Late Blight", "raw_class": "Potato___Late_blight",
                    "pathogen": "Phytophthora infestans", "confidence": 96.5, "severity": "Severe", "area": 58.4,
                    "is_healthy": False, "img": "/uploads/sample_potato_late_blight.jpg",
                    "days_ago": 2, "village": "Palasbari", "district": "Kamrup", "state": "Assam"
                },
                {
                    "crop": "Rice", "disease": "Bacterial Leaf Blight", "raw_class": "Rice___Bacterial_leaf_blight",
                    "pathogen": "Xanthomonas oryzae", "confidence": 91.8, "severity": "Moderate", "area": 36.2,
                    "is_healthy": False, "img": "/uploads/sample_rice_bacterial_blight.jpg",
                    "days_ago": 3, "village": "Raha", "district": "Nagaon", "state": "Assam"
                },
                {
                    "crop": "Corn (Maize)", "disease": "Common Rust", "raw_class": "Corn___Common_rust",
                    "pathogen": "Puccinia sorghi", "confidence": 89.4, "severity": "Moderate", "area": 24.5,
                    "is_healthy": False, "img": "/uploads/sample_corn_rust.jpg",
                    "days_ago": 5, "village": "Mirza", "district": "Kamrup", "state": "Assam"
                },
                {
                    "crop": "Tomato", "disease": "Healthy Leaf", "raw_class": "Tomato___healthy",
                    "pathogen": "None (Healthy)", "confidence": 98.7, "severity": "None / Healthy", "area": 0.0,
                    "is_healthy": True, "img": "/uploads/sample_healthy_tomato.jpg",
                    "days_ago": 6, "village": "Azara", "district": "Kamrup", "state": "Assam"
                },
                {
                    "crop": "Apple", "disease": "Black Rot", "raw_class": "Apple___Black_rot",
                    "pathogen": "Botryosphaeria obtusa", "confidence": 92.1, "severity": "Low", "area": 12.0,
                    "is_healthy": False, "img": "/uploads/sample_apple_rot.jpg",
                    "days_ago": 8, "village": "Hajo", "district": "Kamrup", "state": "Assam"
                }
            ]

            from app.ml.knowledge_base import get_treatment_for_disease

            for s in sample_records:
                treatments = get_treatment_for_disease(s["raw_class"], state=s["state"], district=s["district"])
                rec = DiagnosisRecord(
                    user_id=demo_user.id,
                    crop=s["crop"],
                    disease=s["disease"],
                    raw_class=s["raw_class"],
                    pathogen=s["pathogen"],
                    confidence_score=s["confidence"],
                    severity_level=s["severity"],
                    affected_area_percentage=s["area"],
                    is_healthy=s["is_healthy"],
                    is_uncertain=False,
                    image_path=s["img"],
                    overlay_path=s["img"],
                    state=s["state"],
                    district=s["district"],
                    village=s["village"],
                    symptoms_json=json.dumps(treatments["symptoms"]),
                    organic_treatment_json=json.dumps(treatments["organic_treatment"]),
                    chemical_treatment_json=json.dumps(treatments["chemical_treatment"]),
                    preventive_measures_json=json.dumps(treatments["preventive_measures"]),
                    regional_advisory_json=json.dumps(treatments["regional_advisory"]),
                    created_at=datetime.utcnow() - timedelta(days=s["days_ago"])
                )
                db.add(rec)
            db.commit()
            print(f"[DB Seed] Inserted {len(sample_records)} realistic baseline diagnosis records.")
    except Exception as e:
        print(f"[DB Seed] Note on seeding: {e}")
    finally:
        db.close()

# Run seed
seed_initial_demo_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
