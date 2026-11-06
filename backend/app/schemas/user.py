"""
TAH-015: User Schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    state: Optional[str] = "Assam"
    district: Optional[str] = "Kamrup"
    village: Optional[str] = "Azara"
    farm_size_acres: Optional[float] = 2.5
    preferred_language: Optional[str] = "en"
    primary_crops: Optional[str] = "Tomato, Rice, Potato"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None
    farm_size_acres: Optional[float] = None
    preferred_language: Optional[str] = None
    primary_crops: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
