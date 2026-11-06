"""
TAH-015: Farmer Dashboard Intelligence Router
Aggregates diagnosis statistics, severity distributions, disease frequency charts,
and crop health summary for Recharts visualization.
"""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db
from app.models.user import User
from app.models.diagnosis import DiagnosisRecord
from app.schemas.common import DashboardStats
from app.utils.auth_utils import get_optional_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_statistics(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Computes real diagnosis metrics from the database:
    - Total scans
    - Healthy vs Infected
    - Severe alert count
    - Severity pie breakdown
    - Crop distribution breakdown
    - Top detected diseases
    - Recent diagnosis records
    """
    base_query = db.query(DiagnosisRecord)
    if current_user:
        base_query = base_query.filter(DiagnosisRecord.user_id == current_user.id)

    total_count = base_query.count()

    # If database is completely empty (e.g. brand new installation), provide baseline seed data
    if total_count == 0:
        return DashboardStats(
            total_diagnoses=0,
            healthy_count=0,
            infected_count=0,
            severe_alert_count=0,
            health_index_percentage=100.0,
            severity_distribution=[
                {"name": "None / Healthy", "value": 0, "color": "#10b981"},
                {"name": "Low (<20%)", "value": 0, "color": "#84cc16"},
                {"name": "Moderate (20-50%)", "value": 0, "color": "#f59e0b"},
                {"name": "Severe (>50%)", "value": 0, "color": "#ef4444"}
            ],
            crop_distribution=[],
            frequently_detected_diseases=[],
            recent_diagnoses=[]
        )

    healthy_count = base_query.filter(DiagnosisRecord.is_healthy == True).count()
    infected_count = total_count - healthy_count
    severe_count = base_query.filter(DiagnosisRecord.severity_level == "Severe").count()
    moderate_count = base_query.filter(DiagnosisRecord.severity_level == "Moderate").count()
    low_count = base_query.filter(DiagnosisRecord.severity_level == "Low").count()

    # Health Index %
    health_index = round((healthy_count / total_count) * 100.0, 1)

    severity_dist = [
        {"name": "None / Healthy", "value": healthy_count, "color": "#10b981"},
        {"name": "Low (<20%)", "value": low_count, "color": "#84cc16"},
        {"name": "Moderate (20-50%)", "value": moderate_count, "color": "#f59e0b"},
        {"name": "Severe (>50%)", "value": severe_count, "color": "#ef4444"}
    ]

    # Crop breakdown
    crop_counts = (
        db.query(DiagnosisRecord.crop, func.count(DiagnosisRecord.id))
        .group_by(DiagnosisRecord.crop)
        .all()
    )
    crop_dist = [{"crop": c[0], "count": c[1]} for c in crop_counts]

    # Frequent diseases
    disease_counts = (
        db.query(DiagnosisRecord.disease, DiagnosisRecord.crop, func.count(DiagnosisRecord.id))
        .filter(DiagnosisRecord.is_healthy == False)
        .group_by(DiagnosisRecord.disease, DiagnosisRecord.crop)
        .order_by(desc(func.count(DiagnosisRecord.id)))
        .limit(6)
        .all()
    )
    frequent_diseases = [
        {"disease": d[0], "crop": d[1], "occurrences": d[2]}
        for d in disease_counts
    ]

    # Recent 5 diagnoses
    recent = (
        base_query.order_by(desc(DiagnosisRecord.created_at))
        .limit(5)
        .all()
    )
    recent_items = []
    for r in recent:
        recent_items.append({
            "id": r.id,
            "crop": r.crop,
            "disease": r.disease,
            "confidence_score": r.confidence_score,
            "severity_level": r.severity_level,
            "affected_area_percentage": r.affected_area_percentage,
            "image_url": r.image_path,
            "overlay_url": r.overlay_path,
            "created_at": r.created_at.strftime("%d %b %Y, %I:%M %p") if r.created_at else ""
        })

    return DashboardStats(
        total_diagnoses=total_count,
        healthy_count=healthy_count,
        infected_count=infected_count,
        severe_alert_count=severe_count,
        health_index_percentage=health_index,
        severity_distribution=severity_dist,
        crop_distribution=crop_dist,
        frequently_detected_diseases=frequent_diseases,
        recent_diagnoses=recent_items
    )
