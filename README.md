# Cardiac Attack Prediction Using Deep Learning (with Authentication)

A Full-Stack Mini-Project to predict heart attack risk using vitals and stress levels, powered by Deep Learning.
Now includes **User Authentication** (Signup/Login).

## Key Features
- **Deep Learning Model**: Uses a Multi-Layer Perceptron (MLP) Neural Network trained on heart health data.
- **User Authentication**: Secure Signup and Login using JWT and SQLite.
- **Protected Prediction**: Only logged-in users can access the prediction tool.
- **Interactive UI**: Modern React-based frontend with Dark Mode and responsive design.
- **Real-time Prediction**: Returns risk probability instantly via FastAPI backend.
- **SMS Alerts**: Automatically sends SMS alerts (via Twilio) if risk > 70%.

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
API will run at `http://localhost:8000`.

### 5. Start Frontend
Open a new terminal:
```bash
cd client
npm install
npm run dev
```
App will run at `http://localhost:5173`.

## Usage
1. Open `http://localhost:5173`.
2. You will be redirected to **Login**.
3. Click **Sign up** to create an account.
4. Log in with your new credentials.
5. You will see the **Cardiac Risk Predictor** form.
6. Enter patient details and click **Predict Risk**.

## Project Structure
- `generate_data.py`: Data generation script.
- `train_model.py`: Model training script.
- `backend/`
    - `auth/`: Authentication logic (Utils, Routes).
    - `main.py`: FastAPI application.
    - `database.py`, `models.py`: Database setup.
- `client/`
    - `src/components/`: Login, Signup, Home components.
    - `src/context/`: Auth Context.
