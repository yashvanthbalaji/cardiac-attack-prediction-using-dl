import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import joblib

def train():
    # Load data
    try:
        df = pd.read_csv('heart_data.csv')
    except FileNotFoundError:
        print("Error: 'heart_data.csv' not found. Please run generate_data.py first.")
        return

    X = df.drop('output', axis=1)
    y = df['output']

    # Define categorical and numerical features
    categorical_features = ['cp', 'restecg', 'slope', 'thal']
    numerical_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'bmi', 'stress_level']
    pass_through_features = ['sex', 'fbs', 'exang', 'ca'] 
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('pass', 'passthrough', pass_through_features)
        ])

    # Build Pipeline with MLPClassifier (Neural Network)
    # 2 hidden layers with 64 and 32 neurons, ReLU activation
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', solver='adam', max_iter=500, random_state=42))
    ])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    print("Training MLP Neural Network...")
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.4f}")

    # Save entire pipeline (includes preprocessor + model)
    joblib.dump(model, 'model_pipeline.pkl')
    print("Model pipeline saved to model_pipeline.pkl")

if __name__ == "__main__":
    train()

