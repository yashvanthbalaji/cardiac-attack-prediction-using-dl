import pandas as pd
import numpy as np

def generate_lifestyle_data(num_samples=1000):
    np.random.seed(101)
    # Cardiovascular Disease Dataset (Lifestyle)
    # age (days->years), gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, cardio
    
    data = {
        'age': np.random.randint(30, 85, num_samples),
        'gender': np.random.choice([1, 2], num_samples), # 1: Women, 2: Men (Dataset convention)
        'height': np.random.randint(150, 200, num_samples), # cm
        'weight': np.random.randint(50, 120, num_samples), # kg
        'ap_hi': np.random.randint(110, 180, num_samples), # Systolic
        'ap_lo': np.random.randint(70, 120, num_samples), # Diastolic
        'cholesterol': np.random.choice([1, 2, 3], num_samples), # 1: Normal, 2: Above, 3: Well Above
        'gluc': np.random.choice([1, 2, 3], num_samples), # Glucose
        'smoke': np.random.choice([0, 1], num_samples, p=[0.8, 0.2]),
        'alco': np.random.choice([0, 1], num_samples, p=[0.9, 0.1]),
        'active': np.random.choice([0, 1], num_samples, p=[0.2, 0.8]),
    }
    
    df = pd.DataFrame(data)
    
    # BMI approx
    df['bmi'] = df['weight'] / ((df['height']/100)**2)
    
    # Logic for target (Long Term Risk)
    risk_score = (
        (df['age'] > 60).astype(int) * 0.3 +
        (df['ap_hi'] > 140).astype(int) * 0.3 +
        (df['smoke'] == 1).astype(int) * 0.2 +
        (df['active'] == 0).astype(int) * 0.2 +
        (df['cholesterol'] == 3).astype(int) * 0.2 + 
        (df['bmi'] > 30).astype(int) * 0.2
    )
    prob = (risk_score - risk_score.min()) / (risk_score.max() - risk_score.min())
    prob += np.random.normal(0, 0.1, num_samples)
    df['cardio'] = (prob > 0.45).astype(int)
    
    df.to_csv('data_lifestyle.csv', index=False)
    print("Generated data_lifestyle.csv")

if __name__ == "__main__":
    generate_lifestyle_data()
