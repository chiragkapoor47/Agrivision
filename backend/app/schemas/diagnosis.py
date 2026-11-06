"""
TAH-015: Diagnosis Schemas
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SeverityInfo(BaseModel):
    level: str # "Low", "Moderate", "Severe", "None / Healthy"
    affected_area_percentage: float
    is_reliable: bool
    explanation: str
    overlay_url: Optional[str] = None
    lesion_count: int = 0

class OrganicTreatment(BaseModel):
    title: str
    remedies: List[str]

class ChemicalTreatment(BaseModel):
    title: str
    active_ingredients: List[str]
    application_method: str
    safety_precautions: str
    pre_harvest_interval_days: int

class RegionalAdvisory(BaseModel):
    zone: str
    location_queried: str
    climate_notes: str
    prevention_emphasis: str
    seasonal_care: str
    weather_risk_threshold: str

class TopCandidate(BaseModel):
    crop: str
    disease: str
    confidence: float

class DiagnosisResponse(BaseModel):
    id: Optional[int] = None
    crop: str
    disease: str
    raw_class: str
    pathogen: Optional[str] = ""
    confidence_score: float
    is_uncertain: bool
    confidence_status: str
    is_healthy: bool
    top_candidates: Optional[List[TopCandidate]] = []
    severity: SeverityInfo
    symptoms: List[str]
    organic_treatment: OrganicTreatment
    chemical_treatment: ChemicalTreatment
    preventive_measures: List[str]
    regional_advisory: RegionalAdvisory
    image_url: str
    overlay_url: Optional[str] = None
    created_at: Optional[datetime] = None
    disclaimer: str

class DiagnosisHistoryItem(BaseModel):
    id: int
    crop: str
    disease: str
    confidence_score: float
    severity_level: str
    affected_area_percentage: float
    is_healthy: bool
    is_uncertain: bool
    image_url: str
    overlay_url: Optional[str] = None
    location_summary: str
    created_at: datetime

    class Config:
        from_attributes = True
