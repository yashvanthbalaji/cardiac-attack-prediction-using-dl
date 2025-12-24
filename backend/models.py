from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, nullable=True)
    password_hash = Column(String)

    profile = relationship("Profile", back_populates="user", uselist=False)
    predictions = relationship("Prediction", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    age = Column(Integer)
    gender = Column(String) # 'Male' or 'Female'
    height = Column(Float) # in cm
    weight = Column(Float) # in kg
    bmi = Column(Float)
    medical_conditions = Column(String, nullable=True)
    stress_level = Column(Integer)
    
    # New Lifestyle Fields
    glucose = Column(Integer, default=1) # 1:Normal, 2:Above, 3:High
    smoke = Column(Integer, default=0) # 0/1
    alco = Column(Integer, default=0) # 0/1
    active = Column(Integer, default=1) # 0/1

    user = relationship("User", back_populates="profile")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_type = Column(String, default="acute") # 'acute', 'lifestyle', 'synthetic'
    input_data = Column(String) 
    risk_probability = Column(Float)
    risk_label = Column(String)

    user = relationship("User", back_populates="predictions")
