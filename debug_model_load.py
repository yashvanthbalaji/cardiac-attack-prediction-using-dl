import joblib
import os
import sys
import traceback

def test_load():
    print(f"Current Working Directory: {os.getcwd()}")
    
    files = ['model_uci.pkl', 'model_lifestyle.pkl', 'model_synthetic.pkl']
    for f in files:
        if os.path.exists(f):
            print(f"Found {f} ({os.path.getsize(f)} bytes)")
        else:
            print(f"MISSING {f}")

    print("\nAttempting to load models...")
    
    # UCI
    print("-" * 20)
    try:
        print("Loading model_uci.pkl...")
        model = joblib.load('model_uci.pkl')
        print("SUCCESS: model_uci.pkl loaded")
        print(f"Type: {type(model)}")
    except Exception:
        print("FAILED: model_uci.pkl")
        traceback.print_exc()

    # Lifestyle
    print("-" * 20)
    try:
        print("Loading model_lifestyle.pkl...")
        model = joblib.load('model_lifestyle.pkl')
        print("SUCCESS: model_lifestyle.pkl loaded")
    except Exception:
        print("FAILED: model_lifestyle.pkl")
        traceback.print_exc()

    # Synthetic
    print("-" * 20)
    try:
        print("Loading model_synthetic.pkl...")
        model = joblib.load('model_synthetic.pkl')
        print("SUCCESS: model_synthetic.pkl loaded")
    except Exception:
        print("FAILED: model_synthetic.pkl")
        traceback.print_exc()

if __name__ == "__main__":
    test_load()
