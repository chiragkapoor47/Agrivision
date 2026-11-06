"""
TAH-015: Diagnosis History Record Model
Stores leaf images, segmentation overlays, detected pathogens, confidence,
severity percentage, full treatment advice, and farmer geolocations.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DiagnosisRecord(Base):
    __tablename__ = "diagnosis_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Identification
    crop = Column(String(80), nullable=False, index=True)
    disease = Column(String(120), nullable=False, index=True)
    raw_class = Column(String(120), nullable=True)
    pathogen = Column(String(150), nullable=True)
    confidence_score = Column(Float, nullable=False)
    
    # Severity Assessment
    severity_level = Column(String(30), nullable=False) # "Low", "Moderate", "Severe", "None / Healthy"
    affected_area_percentage = Column(Float, default=0.0)
    is_healthy = Column(Boolean, default=False)
    is_uncertain = Column(Boolean, default=False)
    
    # Media paths
    image_path = Column(String(255), nullable=False)
    overlay_path = Column(String(255), nullable=True)
    
    # Farmer geolocation
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    village = Column(String(100), nullable=True)
    
    # Structured JSON stores for rapid lookup and history viewing
    symptoms_json = Column(Text, nullable=True)
    organic_treatment_json = Column(Text, nullable=True)
    chemical_treatment_json = Column(Text, nullable=True)
    preventive_measures_json = Column(Text, nullable=True)
    regional_advisory_json = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationship
    user = relationship("User", back_populates="diagnoses")
