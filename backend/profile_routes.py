from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from .database import get_db
from .models import User, Profile, Prediction
from .auth.utils import get_current_user
import json

router = APIRouter(prefix="/profile", tags=["Profile"])

class ProfileBase(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    medical_conditions: Optional[str] = None
    stress_level: int
    glucose: int = 1
    smoke: int = 0
    alco: int = 0
    active: int = 1

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    bmi: float
    
    class Config:
        orm_mode = True

class PredictionResponse(BaseModel):
    id: int
    timestamp: str 
    risk_label: str
    risk_probability: float
    model_type: Optional[str] = "acute"
    
    class Config:
        orm_mode = True

@router.get("/", response_model=Optional[ProfileResponse])
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.profile

@router.post("/", response_model=ProfileResponse)
def create_or_update_profile(profile_data: ProfileBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Calculate BMI
    height_m = profile_data.height / 100
    bmi = round(profile_data.weight / (height_m * height_m), 2)

    if current_user.profile:
        # Update existing
        current_user.profile.age = profile_data.age
        current_user.profile.gender = profile_data.gender
        current_user.profile.height = profile_data.height
        current_user.profile.weight = profile_data.weight
        current_user.profile.bmi = bmi
        current_user.profile.medical_conditions = profile_data.medical_conditions
        current_user.profile.stress_level = profile_data.stress_level
        current_user.profile.glucose = profile_data.glucose
        current_user.profile.smoke = profile_data.smoke
        current_user.profile.alco = profile_data.alco
        current_user.profile.active = profile_data.active
        
        db.commit()
        db.refresh(current_user.profile)
        return current_user.profile
    else:
        # Create new
        new_profile = Profile(
            user_id=current_user.id,
            bmi=bmi,
            **profile_data.dict()
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile

@router.get("/history", response_model=List[PredictionResponse])
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Sort by timestamp desc
    return db.query(Prediction).filter(Prediction.user_id == current_user.id).order_by(Prediction.timestamp.desc()).all()
