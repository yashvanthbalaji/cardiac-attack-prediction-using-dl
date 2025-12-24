import joblib
import pandas as pd
import os

def test_prediction():
    if not os.path.exists('model_uci.pkl'):
        print("Error: model_uci.pkl not found")
        return

    try:
        model = joblib.load('model_uci.pkl')
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # User inputs
    input_data = {
        "age": 50,
        "sex": 1,
        "cp": 0,
        "trestbps": 140,
        "chol": 290,
        "fbs": 0,
        "restecg": 1,
        "thalach": 30,  # User input: 30 (Very low)
        "exang": 0,
        "oldpeak": 1.5,
        "slope": 1,
        "ca": 0,
        "thal": 0
    }
    
    print(f"Input Data: {input_data}")
    
    # Predict
    df = pd.DataFrame([input_data])
    
    # Check probability
    try:
        probs = model.predict_proba(df)
        print(f"\nPrediction Probabilities: {probs}")
        risk_prob = probs[0][1]
        print(f"Risk Probability (Class 1): {risk_prob:.4f}")
        
        # Check prediction class
        pred = model.predict(df)
        print(f"Predicted Class: {pred[0]}")
        
    except Exception as e:
        print(f"Prediction Error: {e}")

if __name__ == "__main__":
    test_prediction()
