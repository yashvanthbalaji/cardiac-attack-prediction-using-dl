import joblib
import pandas as pd
import numpy as np

def test_lifestyle():
    try:
        model = joblib.load('model_lifestyle.pkl')
        print("Model loaded.")
        
        # Input matching Frontend/Backend schema
        # backend calculates BMI, so we must too
        height = 175
        weight = 75
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        input_data = {
            'age': 50 * 365, # Cardio train uses DAYS
            'gender': 2, # 1: Female, 2: Male
            'height': height,
            'weight': weight,
            'ap_hi': 120,
            'ap_lo': 80,
            'cholesterol': 1, # 1: Normal, 2: High, 3: Very High
            'gluc': 1,
            'smoke': 0,
            'alco': 0,
            'active': 1,
            'bmi': bmi
        }
        
        print(f"Input: {input_data}")
        df = pd.DataFrame([input_data])
        
        # Reorder columns to match training?
        # Training used: age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, bmi
        # The DataFrame creation order might matter if Pipeline doesn't use column names strictly.
        # ColumnTransformer usually relies on names if configured so.
        
        prob = model.predict_proba(df)[0][1]
        print(f"Prediction Probability: {prob:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_lifestyle()
