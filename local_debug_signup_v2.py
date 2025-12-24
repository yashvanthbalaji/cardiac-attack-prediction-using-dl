from backend.auth.routes import signup, UserCreate
from backend.database import SessionLocal
from backend.models import User
from fastapi import HTTPException

def test_local_signup():
    db = SessionLocal()
    # Cleanup previous test
    existing = db.query(User).filter(User.email == "test_debug@example.com").first()
    if existing:
        db.delete(existing)
        db.commit()

    user_data = UserCreate(
        email="test_debug@example.com",
        password="password123",
        full_name="Debug User",
        phone_number="+1234567890"
    )
    
    print("Attempting signup...")
    try:
        signup(user_data, db)
        print("Signup successful")
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_local_signup()
