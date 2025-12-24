from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client
from sqlalchemy.orm import Session
from .auth import routes as auth_routes
from . import profile_routes
from .database import engine, Base, get_db
from .models import Prediction, User
from .auth.utils import get_current_user

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(profile_routes.router)

# Load Model Pipeline (includes preprocessor + model)
model_pipeline = None

# Load Model Pipelines
models = {
    "uci": None,
    "lifestyle": None,
    "synthetic": None
}

@app.on_event("startup")
def load_artifacts():
    global models
    import traceback
    try:
        models["uci"] = joblib.load('model_uci.pkl')
        print("Model UCI loaded.")
    except Exception as e:
        print(f"FATAL: Model UCI failed to load: {e}")
        traceback.print_exc()
    
    try:
        models["lifestyle"] = joblib.load('model_lifestyle.pkl')
        print("Model Lifestyle loaded.")
    except Exception as e:
        print(f"FATAL: Model Lifestyle failed to load: {e}")
        traceback.print_exc()
    
    try:
        models["synthetic"] = joblib.load('model_synthetic.pkl')
        print("Model Synthetic loaded.")
    except Exception as e:
        print(f"FATAL: Model Synthetic failed to load: {e}")
        traceback.print_exc()

# Input Schemas
class AcuteInput(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    phone_number: str = None

class LifestyleInput(BaseModel):
    # Only fields not in Profile or overrideable
    # Ideally frontend sends everything merged
    age: int
    gender: int
    height: float
    weight: float
    ap_hi: int
    ap_lo: int
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int
    phone_number: str = None

class SyntheticInput(BaseModel):
    stress_level: int
    sleep_hours: float
    daily_steps: int
    water_intake: float
    hrv: int
    age: int
    bmi: float

# Twilio Config (Same as before)
TWILIO_SID = os.getenv("TWILIO_SID", "AC_MOCK_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "MOCK_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")

def send_sms(to_number, risk_score, model_name):
    if not to_number: return
    msg = f"WARNING: High {model_name} Risk ({risk_score*100:.1f}%). Consult doctor."
    try:
        if TWILIO_SID == "AC_MOCK_SID":
            print(f"[MOCK SMS] To: {to_number} | {msg}")
        else:
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(body=msg, from_=TWILIO_PHONE_NUMBER, to=to_number)
    except Exception as e: print(f"SMS Failed: {e}")

def save_history(db, user, data, prob, label, m_type):
    try:
        new_pred = Prediction(
            user_id=user.id,
            model_type=m_type,
            input_data=json.dumps(data),
            risk_probability=prob,
            risk_label=label
        )
        db.add(new_pred)
        db.commit()
    except Exception as e: print(f"History Save Error: {e}")

# --- Endpoints ---

def get_risk_message(prob):
    p = prob * 100
    if p == 0: return "No immediate cardiac risk detected based on current input."
    if 0 < p <= 20: return "Low cardiac risk. Maintain a healthy lifestyle."
    if 20 < p <= 50: return "Moderate cardiac risk. Lifestyle changes and monitoring recommended."
    if 50 < p <= 80: return "High cardiac risk. Medical consultation advised."
    if 80 < p < 100: return "Very high cardiac risk. Seek medical attention soon."
    if p >= 100: return "Extremely high cardiac risk detected. Please visit the nearest hospital immediately."
    return "Unknown risk level." # Fallback

@app.post("/predict") # Keep legacy endpoint mapping to Acute
@app.post("/predict/acute")
def predict_acute(data: AcuteInput, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not models["uci"]: raise HTTPException(503, "Model UCI not loaded")
    
    input_dict = data.dict(exclude={'phone_number'})
    
    try:
        probs = models["uci"].predict_proba(pd.DataFrame([input_dict]))
        risk_prob = float(probs[0][1])
    except Exception as e: raise HTTPException(400, f"Error: {e}")

    label = get_risk_message(risk_prob)
    save_history(db, current_user, input_dict, risk_prob, label, "acute")
    
    if risk_prob > 0.5: send_sms(data.phone_number, risk_prob, "Acute Heart Attack")
    
    return {"risk_probability": risk_prob, "risk_label": label, "alert_sent": risk_prob > 0.5}

@app.post("/predict/lifestyle")
def predict_lifestyle(data: LifestyleInput, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not models["lifestyle"]: raise HTTPException(503, "Model Lifestyle not loaded")
    
    input_dict = data.dict(exclude={'phone_number'})
    
    # CRITICAL FIX: Cardio Train dataset uses age in DAYS. User inputs YEARS.
    # Convert Years -> Days
    input_dict['age'] = input_dict['age'] * 365
    
    height_m = input_dict['height'] / 100
    input_dict['bmi'] = input_dict['weight'] / (height_m * height_m)
    
    try:
        probs = models["lifestyle"].predict_proba(pd.DataFrame([input_dict]))
        risk_prob = float(probs[0][1])
    except Exception as e: raise HTTPException(400, f"Error: {e}")
    
    label = get_risk_message(risk_prob)
    save_history(db, current_user, input_dict, risk_prob, label, "lifestyle")
    
    return {"risk_probability": risk_prob, "risk_label": label}

@app.post("/predict/synthetic")
def predict_synthetic(data: SyntheticInput):
    # No Auth/History required for synthetic as per plan
    if not models["synthetic"]: raise HTTPException(503, "Model Synthetic not loaded")
    
    input_dict = data.dict()
    try:
        risk_score = float(models["synthetic"].predict(pd.DataFrame([input_dict]))[0])
        risk_score = max(0.0, min(1.0, risk_score)) # Clamp 0-1
    except Exception as e: raise HTTPException(400, f"Error: {e}")
    
    return {"risk_probability": risk_score, "risk_label": "Simulated Score"}

@app.get("/")
def read_root():
    return {"message": "Cardiac Prediction API is running"}
