"""
TAH-015: Authentication & Farmer Profile Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate, Token
from app.utils.auth_utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_farmer(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new farmer account"""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A farmer account with this email address already exists."
        )

    db_user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        phone=user_in.phone,
        state=user_in.state or "Assam",
        district=user_in.district or "Kamrup",
        village=user_in.village or "Azara",
        farm_size_acres=user_in.farm_size_acres or 2.5,
        preferred_language=user_in.preferred_language or "en",
        primary_crops=user_in.primary_crops or "Tomato, Rice, Potato"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token({"sub": str(db_user.id), "email": db_user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": db_user
    }

@router.post("/login", response_model=Token)
def login_farmer(credentials: UserLogin, db: Session = Depends(get_db)):
    """Sign in existing farmer"""
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password. Please verify credentials."
        )

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_farmer_profile(current_user: User = Depends(get_current_user)):
    """Retrieve logged in farmer profile"""
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_farmer_profile(
    updates: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update farmer profile, location, and preferred language"""
    update_data = updates.dict(exclude_unset=True)
    for field, val in update_data.items():
        if val is not None:
            setattr(current_user, field, val)

    db.commit()
    db.refresh(current_user)
    return current_user
