import requests
import sys

BASE_URL = "http://localhost:8006"

def run_test():
    print("=== STARTING FULL APP HEALTH CHECK ===")
    
    # 1. SIGNUP
    print("\n[1] Testing Signup...")
    email = "full_test_user@example.com"
    pwd = "password123"
    signup_payload = {
        "email": email,
        "password": pwd,
        "full_name": "Health Check User",
        "phone_number": "+15550199"
    }
    r = requests.post(f"{BASE_URL}/auth/signup", json=signup_payload)
    if r.status_code == 200:
        print("✅ Signup Success")
    elif r.status_code == 400 and "already registered" in r.text:
         print("⚠️ User already exists (OK)")
    else:
        print(f"❌ Signup Failed: {r.status_code} {r.text}")
        sys.exit(1)

    # 2. LOGIN
    print("\n[2] Testing Login...")
    login_payload = {"username": email, "password": pwd}
    r = requests.post(f"{BASE_URL}/auth/login", data=login_payload)
    if r.status_code != 200:
        print(f"❌ Login Failed: {r.status_code} {r.text}")
        sys.exit(1)
    
    token = r.json().get("access_token")
    if not token:
        print("❌ No token returned")
        sys.exit(1)
    print("✅ Login Success (Token received)")
    
    headers = {"Authorization": f"Bearer {token}"}

    # 3. PROFILE CREATION
    print("\n[3] Testing Profile Creation (with new Lifestyle fields)...")
    profile_payload = {
        "age": 45, "gender": "Male", "height": 175, "weight": 80,
        "medical_conditions": "None", "stress_level": 4,
        "glucose": 1, "smoke": 0, "alco": 1, "active": 1
    }
    r = requests.post(f"{BASE_URL}/profile/", json=profile_payload, headers=headers)
    if r.status_code == 200:
        # Verify fields came back
        p = r.json()
        if p.get('glucose') == 1 and p.get('alco') == 1:
            print("✅ Profile Created & Verified")
        else:
            print(f"❌ Profile Saved but fields missing: {p}")
            sys.exit(1)
    else:
        print(f"❌ Profile Creation Failed: {r.status_code} {r.text}")
        sys.exit(1)

    # 4. ACUTE PREDICTION (Using Frontend-style payload)
    print("\n[4] Testing Acute Heart Attack Prediction...")
    acute_payload = {
        "age": 45, "sex": 1, "cp": 0, "trestbps": 130, "chol": 200, "fbs": 0,
        "restecg": 0, "thalach": 160, "exang": 0, "oldpeak": 1.0, "slope": 1,
        "ca": 0, "thal": 2,
        "stress_level": 4, "bmi": 26.1, "phone_number": "" # Extra fields FE sends
    }
    r = requests.post(f"{BASE_URL}/predict/acute", json=acute_payload, headers=headers)
    if r.status_code == 200:
        print(f"✅ Acute Prediction Success: {r.json()['risk_probability']:.2f} ({r.json()['risk_label']})")
    else:
        print(f"❌ Acute Prediction Failed: {r.status_code} {r.text}")
        sys.exit(1)

    # 5. LIFESTYLE PREDICTION
    print("\n[5] Testing Lifestyle Prediction...")
    # FE constructs this from profile
    lifestyle_payload = {
        "age": 45, "gender": 2, "height": 175, "weight": 80,
        "ap_hi": 120, "ap_lo": 80, "cholesterol": 1,
        "gluc": 1, "smoke": 0, "alco": 1, "active": 1
    }
    r = requests.post(f"{BASE_URL}/predict/lifestyle", json=lifestyle_payload, headers=headers)
    if r.status_code == 200:
        print(f"✅ Lifestyle Prediction Success: {r.json()['risk_probability']:.2f} ({r.json()['risk_label']})")
    else:
        print(f"❌ Lifestyle Prediction Failed: {r.status_code} {r.text}")
        sys.exit(1)

    # 6. SYNTHETIC PREDICTION
    print("\n[6] Testing Synthetic Simulation...")
    syn_payload = {
        "stress_level": 8, "sleep_hours": 5, "daily_steps": 2000,
        "water_intake": 1, "hrv": 40, "age": 45, "bmi": 26.1
    }
    r = requests.post(f"{BASE_URL}/predict/synthetic", json=syn_payload)
    if r.status_code == 200:
        print(f"✅ Synthetic Sim Success: {r.json()['risk_probability']:.2f}")
    else:
        print(f"❌ Synthetic Sim Failed: {r.status_code} {r.text}")
        sys.exit(1)

    print("\n=== ALL SYSTEM CHECKS PASSED ===")

if __name__ == "__main__":
    run_test()
