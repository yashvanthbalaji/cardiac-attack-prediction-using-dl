import requests
import json

def test_signup():
    url = "http://127.0.0.1:8001/auth/signup"
    payload = {
        "email": "test_port8001@example.com",
        "password": "password123",
        "full_name": "Test User 8001",
        "phone_number": "+1234567890"
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_signup()
