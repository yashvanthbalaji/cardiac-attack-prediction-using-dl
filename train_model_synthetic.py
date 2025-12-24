import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

def train_synthetic():
    try:
        df = pd.read_csv('data_synthetic.csv')
    except FileNotFoundError:
        import generate_synthetic_data
        generate_synthetic_data.generate_synthetic_data()
        df = pd.read_csv('data_synthetic.csv')

    X = df.drop('synthetic_risk', axis=1)
    y = df['synthetic_risk'] 

    # Regression task for score, or classification? Plan said "Simulated Risk Simulation".
    # Let's keep it as a regression score 0-1.
    
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression()) 
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)
    model.fit(X_train, y_train)
    print(f"Model Synthetic R2 Score: {model.score(X_test, y_test):.4f}")

    joblib.dump(model, 'model_synthetic.pkl')
    print("Saved model_synthetic.pkl")

if __name__ == "__main__":
    train_synthetic()
