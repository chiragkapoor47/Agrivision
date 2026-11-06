"""
TAH-015: Farmer User Model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(25), nullable=True)
    
    # Regional Location details for localized agronomic advice
    state = Column(String(100), default="Assam")
    district = Column(String(100), default="Kamrup")
    village = Column(String(100), default="Azara")
    farm_size_acres = Column(Float, default=2.5)
    
    # Multi-language preference ('en', 'hi', 'as')
    preferred_language = Column(String(10), default="en")
    primary_crops = Column(String(255), default="Tomato, Rice, Potato")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    diagnoses = relationship("DiagnosisRecord", back_populates="user", cascade="all, delete-orphan")
