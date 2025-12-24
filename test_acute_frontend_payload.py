import requests
import json

BASE_URL = "http://localhost:8005"

def test_frontend_payload():
    # Login first
    email = "debug_payload@example.com"
    pwd = "password123"
    
    # Signup/Login to get token
    requests.post(f"{BASE_URL}/auth/signup", json={"email":email, "password":pwd, "full_name":"Debug", "phone_number":""})
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username":email, "password":pwd})
    if resp.status_code != 200:
        print("Login failed")
        return
    token = resp.json()["access_token"]
    
    # Exact payload from Home.jsx
    payload = {
        "age": 55,
        "sex": 1,
        "cp": 0,
        "trestbps": 140,
        "chol": 240,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.5,
        "slope": 1,
        "ca": 0,
        "thal": 2,
        "stress_level": 5,      # Extra field
        "bmi": 25.0,            # Extra field
        "phone_number": ""
    }
    
    print("Sending Frontend Payload...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE_URL}/predict/acute", json=payload, headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")

if __name__ == "__main__":
    test_frontend_payload()
