import pandas as pd
import numpy as np

def generate_uci_data(num_samples=1000):
    np.random.seed(42)
    # UCI Heart Disease Structure
    # age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target
    
    data = {
        'age': np.random.randint(29, 78, num_samples),
        'sex': np.random.choice([0, 1], num_samples),
        'cp': np.random.choice([0, 1, 2, 3], num_samples), # 0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic
        'trestbps': np.random.randint(94, 200, num_samples),
        'chol': np.random.randint(126, 564, num_samples),
        'fbs': np.random.choice([0, 1], num_samples), # > 120 mg/dl
        'restecg': np.random.choice([0, 1, 2], num_samples),
        'thalach': np.random.randint(30, 202, num_samples), # Widen range to include user input
        'exang': np.random.choice([0, 1], num_samples),
        'oldpeak': np.round(np.random.uniform(0, 6.2, num_samples), 1),
        'slope': np.random.choice([0, 1, 2], num_samples),
        'ca': np.random.choice([0, 1, 2, 3, 4], num_samples),
        'thal': np.random.choice([0, 1, 2, 3], num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Logic for target (Acute Heart Attack Risk)
    # Improved logic to match medical reality better for demo purposes
    # Aggressively weighting high cholesterol/BP for demonstration
    risk_score = (
        (df['age'] > 55).astype(int) * 0.2 +
        (df['cp'] > 0).astype(int) * 0.3 + 
        (df['oldpeak'] > 2.0).astype(int) * 0.3 +
        (df['thal'] == 2).astype(int) * 0.2 +
        (df['ca'] > 0).astype(int) * 0.2 +
        (df['chol'] > 250).astype(int) * 2.0 +  # Massive weight
        (df['trestbps'] > 130).astype(int) * 1.5 + # Massive weight
        (df['thalach'] < 100).astype(int) * 0.5 # Low Max HR is bad
    )
    prob = (risk_score - risk_score.min()) / (risk_score.max() - risk_score.min())
    prob += np.random.normal(0, 0.1, num_samples)
    df['target'] = (prob > 0.5).astype(int)
    
    df.to_csv('data_uci.csv', index=False)
    print("Generated data_uci.csv")

if __name__ == "__main__":
    generate_uci_data()
