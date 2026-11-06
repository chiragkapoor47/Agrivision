"""
TAH-015: Prediction & Diagnostic REST API Router
Accepts smartphone leaf photograph, classifies crop and disease with PyTorch,
computes severity via OpenCV lesion segmentation, generates diagnostic mask,
and returns verified organic & chemical treatments.
"""
import json
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.models.user import User
from app.models.diagnosis import DiagnosisRecord
from app.schemas.diagnosis import DiagnosisResponse
from app.utils.auth_utils import get_optional_user
from app.utils.image_utils import validate_and_save_leaf_image
from app.ml.inference import get_inference_engine

router = APIRouter(tags=["AI Disease Detection"])

@router.post("/predict", response_model=DiagnosisResponse)
async def predict_crop_disease(
    file: UploadFile = File(...),
    crop_hint: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    village: Optional[str] = Form(None),
    language: Optional[str] = Form("en"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Core AI Diagnostic Endpoint:
    - Analyzes leaf image with MobileNetV2
    - Identifies crop species & disease
    - Calculates confidence score
    - Measures disease severity percentage (<20% Low, 20-50% Moderate, >50% Severe)
    - Generates visual lesion mask overlay
    - Prescribes localized organic & chemical treatments with active ingredients & PHI
    """
    # 1. Validate & store original uploaded image
    filename, relative_url, raw_bytes = validate_and_save_leaf_image(file)

    # 2. Resolve farmer location & language preferences
    user_state = state or (current_user.state if current_user else "Assam")
    user_district = district or (current_user.district if current_user else "Kamrup")
    user_village = village or (current_user.village if current_user else "Azara")
    user_lang = language or (current_user.preferred_language if current_user else "en")

    # 3. Execute AI Inference + OpenCV Severity Engine
    engine = get_inference_engine()
    inference_result = engine.predict(
        image_data=raw_bytes,
        crop_hint=crop_hint,
        state=user_state,
        district=user_district,
        language=user_lang,
        output_upload_dir=settings.UPLOAD_DIR
    )

    # 4. Save Diagnosis Record in Database
    db_record = DiagnosisRecord(
        user_id=current_user.id if current_user else None,
        crop=inference_result["crop"],
        disease=inference_result["disease"],
        raw_class=inference_result["raw_class"],
        pathogen=inference_result.get("pathogen", ""),
        confidence_score=inference_result["confidence_score"],
        severity_level=inference_result["severity"]["level"],
        affected_area_percentage=inference_result["severity"]["affected_area_percentage"],
        is_healthy=inference_result["is_healthy"],
        is_uncertain=inference_result["is_uncertain"],
        image_path=relative_url,
        overlay_path=inference_result["severity"]["overlay_url"],
        state=user_state,
        district=user_district,
        village=user_village,
        symptoms_json=json.dumps(inference_result["symptoms"]),
        organic_treatment_json=json.dumps(inference_result["organic_treatment"]),
        chemical_treatment_json=json.dumps(inference_result["chemical_treatment"]),
        preventive_measures_json=json.dumps(inference_result["preventive_measures"]),
        regional_advisory_json=json.dumps(inference_result["regional_advisory"])
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    # 5. Build and return structured response
    return DiagnosisResponse(
        id=db_record.id,
        crop=inference_result["crop"],
        disease=inference_result["disease"],
        raw_class=inference_result["raw_class"],
        pathogen=inference_result.get("pathogen", ""),
        confidence_score=inference_result["confidence_score"],
        is_uncertain=inference_result["is_uncertain"],
        confidence_status=inference_result["confidence_status"],
        is_healthy=inference_result["is_healthy"],
        top_candidates=inference_result.get("top_candidates", []),
        severity=inference_result["severity"],
        symptoms=inference_result["symptoms"],
        organic_treatment=inference_result["organic_treatment"],
        chemical_treatment=inference_result["chemical_treatment"],
        preventive_measures=inference_result["preventive_measures"],
        regional_advisory=inference_result["regional_advisory"],
        image_url=relative_url,
        overlay_url=inference_result["severity"]["overlay_url"],
        created_at=db_record.created_at,
        disclaimer=inference_result["disclaimer"]
    )
