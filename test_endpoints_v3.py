import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# 1. Login to get token
def login():
    url = f"{BASE_URL}/auth/login"
    payload = {"username": "test_port8002@example.com", "password": "password123"}
    # Note: user from previous step 'test_port8002' might not exist on port 8000 if user reset DB.
    # Let's try to signup a fresh debug user for this test to be robust.
    return None

def setup_user():
    email = "debug_models@example.com"
    pwd = "password123"
    
    # Signup
    requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email, "password": pwd, "full_name": "Debug Model User", "phone_number": ""
    })
    
    # Login
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": pwd})
    if resp.status_code == 200:
        return resp.json()["access_token"]
    print("Login failed:", resp.text)
    return None

def test_acute(token):
    print("\nTesting Acute Risk...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "age": 55, "sex": 1, "cp": 0, "trestbps": 140, "chol": 240, 
        "fbs": 0, "restecg": 1, "thalach": 150, "exang": 0, 
        "oldpeak": 1.5, "slope": 1, "ca": 0, "thal": 2, "phone_number": ""
    }
    try:
        r = requests.post(f"{BASE_URL}/predict/acute", json=payload, headers=headers)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e: print(e)

def test_lifestyle(token):
    print("\nTesting Lifestyle Risk...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "age": 30, "gender": 2, "height": 175, "weight": 80, 
        "ap_hi": 120, "ap_lo": 80, "cholesterol": 1, "gluc": 1, 
        "smoke": 0, "alco": 0, "active": 1, "phone_number": ""
    }
    try:
        r = requests.post(f"{BASE_URL}/predict/lifestyle", json=payload, headers=headers)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e: print(e)

if __name__ == "__main__":
    token = setup_user()
    if token:
        test_acute(token)
        test_lifestyle(token)
