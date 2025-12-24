import pandas as pd
import numpy as np
import random

def generate_data(num_samples=1000):
    np.random.seed(42)

    data = {
        'age': np.random.randint(20, 80, num_samples),
        'sex': np.random.choice([0, 1], num_samples),  # 0: Female, 1: Male
        'cp': np.random.choice([0, 1, 2, 3], num_samples),  # Chest Pain Type
        'trestbps': np.random.randint(94, 200, num_samples),  # Resting Blood Pressure
        'chol': np.random.randint(126, 564, num_samples),  # Cholesterol
        'fbs': np.random.choice([0, 1], num_samples),  # Fasting Blood Sugar > 120 mg/dl
        'restecg': np.random.choice([0, 1, 2], num_samples),  # Resting Electrocardiographic Results
        'thalach': np.random.randint(71, 202, num_samples),  # Maximum Heart Rate Achieved
        'exang': np.random.choice([0, 1], num_samples),  # Exercise Induced Angina
        'oldpeak': np.round(np.random.uniform(0, 6.2, num_samples), 1),  # ST depression
        'slope': np.random.choice([0, 1, 2], num_samples),  # Slope of the peak exercise ST segment
        'ca': np.random.choice([0, 1, 2, 3, 4], num_samples),  # Number of major vessels
        'thal': np.random.choice([0, 1, 2, 3], num_samples),  # Thalassemia
        'stress_level': np.random.randint(1, 10, num_samples), # Self-reported stress 1-10
        'bmi': np.round(np.random.uniform(18.5, 40.0, num_samples), 1) # Body Mass Index
    }

    df = pd.DataFrame(data)

    # Generate Target Variable based on some logical rules + noise to simulate real world
    # This is a SIMPLIFIED rule just for synthetic data. Real medical data is complex.
    # Higher risk factors increase probability of heart attack (target=1)
    
    risk_score = (
        (df['age'] > 50).astype(int) * 0.2 +
        (df['sex'] == 1).astype(int) * 0.1 +
        (df['cp'] > 0).astype(int) * 0.3 +
        (df['trestbps'] > 140).astype(int) * 0.2 +
        (df['chol'] > 240).astype(int) * 0.2 +
        (df['stress_level'] > 7).astype(int) * 0.2 + 
        (df['bmi'] > 30).astype(int) * 0.15 + 
        (df['exang'] == 1).astype(int) * 0.2 + 
        (df['thal'] == 2).astype(int) * 0.2
    )
    
    # Sigmoid-ish probability
    min_score = risk_score.min()
    max_score = risk_score.max()
    prob = (risk_score - min_score) / (max_score - min_score)
    
    # Add noise
    prob += np.random.normal(0, 0.1, num_samples)
    prob = np.clip(prob, 0, 1)

    df['output'] = (prob > 0.45).astype(int) # slightly lower threshold to account for noise

    output_path = 'heart_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {output_path} with {num_samples} samples.")
    print(df.head())
    return df

if __name__ == "__main__":
    generate_data()
