"""
TAH-015: Diagnosis History & Record Retrieval Router
Allows farmers to inspect previous diagnoses, view overlays, and delete records.
"""
import os
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.config import settings
from app.models.user import User
from app.models.diagnosis import DiagnosisRecord
from app.schemas.diagnosis import DiagnosisHistoryItem, DiagnosisResponse
from app.utils.auth_utils import get_optional_user, get_current_user

router = APIRouter(prefix="/diagnosis", tags=["Diagnosis History"])

@router.get("/history", response_model=List[DiagnosisHistoryItem])
def get_diagnosis_history(
    crop: Optional[str] = Query(None, description="Filter by crop name"),
    severity: Optional[str] = Query(None, description="Filter by severity level (Low, Moderate, Severe)"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Retrieve history of crop disease diagnoses for current farmer (or recent community records)"""
    query = db.query(DiagnosisRecord)

    if current_user:
        query = query.filter(DiagnosisRecord.user_id == current_user.id)

    if crop and crop.lower() not in ["", "all"]:
        query = query.filter(DiagnosisRecord.crop.ilike(f"%{crop}%"))

    if severity and severity.lower() not in ["", "all"]:
        query = query.filter(DiagnosisRecord.severity_level.ilike(f"%{severity}%"))

    records = query.order_by(desc(DiagnosisRecord.created_at)).offset(offset).limit(limit).all()

    items = []
    for r in records:
        loc = ", ".join(filter(None, [r.village, r.district, r.state])) or "Field scan"
        items.append(DiagnosisHistoryItem(
            id=r.id,
            crop=r.crop,
            disease=r.disease,
            confidence_score=r.confidence_score,
            severity_level=r.severity_level,
            affected_area_percentage=r.affected_area_percentage or 0.0,
            is_healthy=bool(r.is_healthy),
            is_uncertain=bool(r.is_uncertain),
            image_url=r.image_path,
            overlay_url=r.overlay_path,
            location_summary=loc,
            created_at=r.created_at
        ))
    return items

@router.get("/{diagnosis_id}", response_model=DiagnosisResponse)
def get_diagnosis_detail(
    diagnosis_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve full diagnosis report by ID including treatments and visual severity overlay"""
    record = db.query(DiagnosisRecord).filter(DiagnosisRecord.id == diagnosis_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis record not found.")

    symptoms = json.loads(record.symptoms_json) if record.symptoms_json else []
    organic_t = json.loads(record.organic_treatment_json) if record.organic_treatment_json else {"title": "Organic Care", "remedies": []}
    chemical_t = json.loads(record.chemical_treatment_json) if record.chemical_treatment_json else {"title": "Chemical Care", "active_ingredients": [], "application_method": "", "safety_precautions": "", "pre_harvest_interval_days": 0}
    preventive = json.loads(record.preventive_measures_json) if record.preventive_measures_json else []
    regional = json.loads(record.regional_advisory_json) if record.regional_advisory_json else {
        "zone": "General Zone", "location_queried": record.district or "Field", "climate_notes": "", "prevention_emphasis": "", "seasonal_care": "", "weather_risk_threshold": ""
    }

    return DiagnosisResponse(
        id=record.id,
        crop=record.crop,
        disease=record.disease,
        raw_class=record.raw_class or "",
        pathogen=record.pathogen or "",
        confidence_score=record.confidence_score,
        is_uncertain=bool(record.is_uncertain),
        confidence_status="Diagnostic Record Retrieved",
        is_healthy=bool(record.is_healthy),
        top_candidates=[],
        severity={
            "level": record.severity_level,
            "affected_area_percentage": record.affected_area_percentage,
            "is_reliable": True,
            "explanation": f"Archived assessment of {record.affected_area_percentage}% leaf area affected.",
            "overlay_url": record.overlay_path,
            "lesion_count": 0
        },
        symptoms=symptoms,
        organic_treatment=organic_t,
        chemical_treatment=chemical_t,
        preventive_measures=preventive,
        regional_advisory=regional,
        image_url=record.image_path,
        overlay_url=record.overlay_path,
        created_at=record.created_at,
        disclaimer="AI Diagnostic Notice: This recommendation is generated via computer vision analysis and does not replace in-person inspection by a certified agricultural extension officer or agronomist."
    )

@router.delete("/{diagnosis_id}")
def delete_diagnosis_record(
    diagnosis_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Delete a diagnosis record"""
    record = db.query(DiagnosisRecord).filter(DiagnosisRecord.id == diagnosis_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis record not found.")

    if current_user and record.user_id and record.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this record.")

    # Clean up associated local image files if present
    for path_attr in [record.image_path, record.overlay_path]:
        if path_attr and path_attr.startswith("/uploads/"):
            fname = path_attr.replace("/uploads/", "")
            full_path = os.path.join(settings.UPLOAD_DIR, fname)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception:
                    pass

    db.delete(record)
    db.commit()
    return {"success": True, "message": f"Diagnosis record #{diagnosis_id} successfully deleted."}
