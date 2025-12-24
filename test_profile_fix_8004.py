import requests
import json

BASE_URL = "http://127.0.0.1:8004"

def test_flow():
    email = "profile_fix_8004@example.com"
    pwd = "password123"
    
    # 1. Signup
    requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email, "password": pwd, "full_name": "Profile Fix User", "phone_number": ""
    })
    
    # 2. Login
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": pwd})
    if resp.status_code != 200:
        print("Login failed")
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Profile with new fields
    profile_data = {
        "age": 40, "gender": "Male", "height": 180, "weight": 85, 
        "medical_conditions": "None", "stress_level": 5,
        "glucose": 2, "smoke": 1, "alco": 0, "active": 1
    }
    print("Updating Profile...")
    r = requests.post(f"{BASE_URL}/profile/", json=profile_data, headers=headers)
    print(f"Update Status: {r.status_code}")
    print(f"Update Response: {r.text}")
    
    # 4. Fetch Profile to verify persistence
    print("\nFetching Profile...")
    r = requests.get(f"{BASE_URL}/profile/", headers=headers)
    p = r.json()
    print(f"Fetched Profile: {p}")
    
    # Check if new fields exist
    if 'glucose' in p and p['glucose'] == 2 and p['smoke'] == 1:
        print("PASS: New fields persisted and returned.")
    else:
        print("FAIL: New fields missing.")

    # 5. Predict Lifestyle
    print("\nTesting Lifestyle Prediction...")
    # Frontend logic: maps profile fields to prediction input
    pred_payload = {
        "age": p['age'],
        "gender": 2 if p['gender'] == 'Male' else 1,
        "height": p['height'],
        "weight": p['weight'],
        "ap_hi": 120, "ap_lo": 80, "cholesterol": 1, 
        "gluc": p['glucose'], # If undefined, this would be None
        "smoke": p['smoke'],
        "alco": p['alco'],
        "active": p['active']
    }
    r = requests.post(f"{BASE_URL}/predict/lifestyle", json=pred_payload, headers=headers)
    print(f"Prediction Status: {r.status_code}")
    print(f"Prediction Response: {r.text}")

if __name__ == "__main__":
    test_flow()
