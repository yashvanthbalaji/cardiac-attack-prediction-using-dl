import requests

BASE_URL = "http://localhost:8000"

def test_auth():
    # 1. Signup
    signup_data = {
        "email": "api_test@test.com",
        "password": "password",
        "full_name": "API Test User",
        "phone_number": "123"
    }
    try:
        r = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        print(f"Signup Status: {r.status_code}")
        print(f"Signup Response: {r.text}")
    except Exception as e:
        print(f"Signup Failed: {e}")

    # 2. Login
    login_data = {
        "username": "api_test@test.com",
        "password": "password"
    }
    try:
        # Testing standard form data
        r = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Login Status: {r.status_code}")
        print(f"Login Response: {r.text}")
        
        if r.status_code == 200:
            token = r.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            r_me = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            print(f"Me Status: {r_me.status_code}")
            print(f"Me Response: {r_me.text}")

    except Exception as e:
        print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_auth()
