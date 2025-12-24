import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import joblib

def train_lifestyle():
    try:
        # Try reading with default comma
        df = pd.read_csv('data_lifestyle.csv')
        if len(df.columns) <= 1: # Likely failed to parse, try semicolon
             df = pd.read_csv('data_lifestyle.csv', sep=';')
             print("Detected semicolon delimiter.")
        
        if 'id' in df.columns:
            df = df.drop('id', axis=1)
            print("Dropped 'id' column.")
            
        # Calculate BMI if missing (Real dataset has weight(kg) and height(cm))
        if 'bmi' not in df.columns:
            # height is in cm in cardio_train
            df['height_m'] = df['height'] / 100
            df['bmi'] = df['weight'] / (df['height_m'] ** 2)
            df = df.drop('height_m', axis=1)
            print("Calculated BMI from height/weight.")
            
    except FileNotFoundError:
        import generate_lifestyle_data
        generate_lifestyle_data.generate_lifestyle_data()
        df = pd.read_csv('data_lifestyle.csv')

    X = df.drop('cardio', axis=1)
    y = df['cardio']

    # age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active
    # Categorical: gender, cholesterol, gluc, smoke, alco, active (already 0/1 or small ints)
    # Numerical: age, height, weight, ap_hi, ap_lo, bmi
    
    numerical_features = ['age', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi']
    categorical_features = ['cholesterol', 'gluc'] # These have 1,2,3 values
    pass_through_features = ['gender', 'smoke', 'alco', 'active']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('pass', 'passthrough', pass_through_features)
        ])

    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', MLPClassifier(hidden_layer_sizes=(32, 16), activation='relu', max_iter=500, random_state=101))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
    model.fit(X_train, y_train)
    print(f"Model Lifestyle Accuracy: {model.score(X_test, y_test):.4f}")

    joblib.dump(model, 'model_lifestyle.pkl')
    print("Saved model_lifestyle.pkl")

if __name__ == "__main__":
    train_lifestyle()
