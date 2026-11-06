"""
TAH-015: Common & Dashboard Schemas
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DashboardStats(BaseModel):
    total_diagnoses: int
    healthy_count: int
    infected_count: int
    severe_alert_count: int
    health_index_percentage: float
    severity_distribution: List[Dict[str, Any]]
    crop_distribution: List[Dict[str, Any]]
    frequently_detected_diseases: List[Dict[str, Any]]
    recent_diagnoses: List[Dict[str, Any]]

class CropItem(BaseModel):
    id: str
    name: str
    name_hi: str
    name_as: str
    scientific_name: str
    common_diseases: List[str]
    ideal_growing_conditions: str
    water_requirements: str
    soil_ph: str

class DiseaseItem(BaseModel):
    id: str
    crop: str
    name: str
    name_hi: str
    name_as: str
    pathogen_type: str
    typical_symptoms: List[str]

class EducationalResource(BaseModel):
    id: str
    category: str # "disease_identification", "organic_farming", "preventive_practices", "crop_care"
    title: str
    title_hi: str
    title_as: str
    summary: str
    summary_hi: str
    summary_as: str
    steps_or_points: List[str]
    read_time_mins: int
    badge: str
