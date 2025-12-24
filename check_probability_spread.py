import joblib
import pandas as pd
import numpy as np

def check_spread():
    try:
        model = joblib.load('model_uci.pkl')
        df = pd.read_csv('data_uci.csv')
        
        # Prepare data (same logic as training)
        possible_targets = ['condition', 'num', 'output', 'target']
        for col in possible_targets:
            if col in df.columns:
                df = df.rename(columns={col: 'target'})
                break
        
        X = df.drop('target', axis=1)
        
        # Predict Proba
        probs = model.predict_proba(X)[:, 1] # Get class 1 probabilities
        
        print(f"Total Samples: {len(probs)}")
        print(f"Min Prob: {probs.min():.4f}")
        print(f"Max Prob: {probs.max():.4f}")
        print(f"Mean Prob: {probs.mean():.4f}")
        
        # Check for nuances
        uniques = np.unique(probs.round(2))
        print(f"Unique probability values (rounded): {len(uniques)}")
        print("Sample raw probabilities:", probs[:10])
        
        if len(uniques) < 5:
            print("CONCLUSION: Model is outputting almost purely binary results.")
        else:
            print("CONCLUSION: Model HAS nuance, but maybe your inputs triggered a confident response.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_spread()
