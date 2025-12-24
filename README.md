# Cardiac Attack Prediction Using Deep Learning (with Authentication)

A full‑stack **mini‑project** that predicts the **risk of a cardiac (heart) attack** using patient vitals and stress‑related parameters. The system is powered by a **Deep Learning MLP model** and secured with **user authentication**. Only authenticated users can access the prediction feature.

This project is designed for **academic mini‑projects**, practical learning, and GitHub portfolio demonstration.

---

## 🔑 Key Features

* **Deep Learning Prediction Model**
  Uses a **Multi‑Layer Perceptron (MLP)** neural network trained on heart‑health data to predict cardiac risk.

* **User Authentication (Signup / Login)**
  Secure authentication implemented using **JWT (JSON Web Tokens)** with **SQLite** as the database.

* **Protected Prediction API**
  Only logged‑in users can access the cardiac risk prediction endpoint.

* **FastAPI Backend**
  High‑performance backend with REST APIs for authentication and prediction.

* **Modern Frontend (React)**
  Responsive UI with clean design, form validation, and dark‑mode‑friendly layout.

* **Real‑Time Risk Prediction**
  Provides instant cardiac risk probability based on user‑entered health parameters.

* **SMS Alert System**
  Automatically sends an SMS alert using **Twilio** when predicted risk exceeds **70%**.

---

## 🧠 Technologies Used

### Backend

* Python
* FastAPI
* TensorFlow / Keras (MLP Model)
* SQLite
* JWT Authentication
* Twilio SMS API
* SMTP for email

### Frontend

* React (Vite)
* JavaScript
* CSS / Modern UI Components

---

## 📁 Project Structure

```
Cardiac-Attack-Prediction/
│
├── generate_data.py        # Synthetic dataset generation
├── train_model.py          # Deep learning model training
│
├── backend/
│   ├── auth/               # Authentication logic
│   │   ├── routes.py
│   │   ├── utils.py
│   ├── main.py              # FastAPI entry point
│   ├── database.py          # SQLite database setup
│   ├── models.py            # ORM models
│
├── client/
│   ├── src/
│   │   ├── components/      # Login, Signup, Home
│   │   ├── context/         # Authentication context
│   │   ├── App.jsx
│   │   ├── main.jsx
│
└── README.md
```

---

## ⚙️ How to Run the Project

### 1️⃣ Backend Setup

```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at:

```
http://localhost:8000
```

---

### 2️⃣ Frontend Setup

Open a new terminal:

```bash
cd client
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

## 🚀 Application Flow

1. Open the application in the browser.
2. User is redirected to the **Login page**.
3. New users create an account using **Signup**.
4. After successful login, user accesses the **Cardiac Risk Predictor**.
5. User enters health details (age, BP, cholesterol, stress level, etc.).
6. The model predicts **heart attack risk percentage**.
7. If risk > 70%, an **SMS alert** is sent automatically.

---

## ⚠️ Disclaimer

This project is **for educational purposes only**. It is **not a medical diagnostic system** and should not be used for real‑world medical decisions.

---
