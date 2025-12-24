import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples=1000):
    np.random.seed(99)
    # Synthetic Simulation Data
    # Purely experimental/simulation based fields
    # stress_level, sleep_hours, daily_steps, water_intake, heart_rate_variability
    
    data = {
        'stress_level': np.random.randint(1, 10, num_samples),
        'sleep_hours': np.random.uniform(4, 10, num_samples),
        'daily_steps': np.random.randint(1000, 15000, num_samples),
        'water_intake': np.random.uniform(0.5, 4.0, num_samples), # Liters
        'hrv': np.random.randint(20, 100, num_samples), # ms
        
        # Core vitals for correlation
        'age': np.random.randint(20, 80, num_samples),
        'bmi': np.random.uniform(18, 35, num_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Logic: High Stress + Low Sleep + Low Steps = Bad Synthetic Score
    score = (
        df['stress_level'] * 0.3 +
        (10 - df['sleep_hours']) * 0.2 +
        (15000 - df['daily_steps'])/1000 * 0.2 +
        (df['bmi'] - 22).abs() * 0.3
    )
    
    # Normalize 0-1
    df['synthetic_risk'] = (score - score.min()) / (score.max() - score.min())
    
    df.to_csv('data_synthetic.csv', index=False)
    print("Generated data_synthetic.csv")

if __name__ == "__main__":
    generate_synthetic_data()
