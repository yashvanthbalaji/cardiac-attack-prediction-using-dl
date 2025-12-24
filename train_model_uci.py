import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import joblib

def train_uci():
    try:
        df = pd.read_csv('data_uci.csv')
        # Normalize target column name
        possible_targets = ['condition', 'num', 'output', 'target']
        for col in possible_targets:
            if col in df.columns:
                df = df.rename(columns={col: 'target'})
                print(f"Renamed column '{col}' to 'target'")
                break
        
        if 'target' not in df.columns:
            print(f"Error: Could not find target column. Available: {df.columns.tolist()}")
            return
            
    except FileNotFoundError:
        import generate_uci_data
        generate_uci_data.generate_uci_data()
        df = pd.read_csv('data_uci.csv')

    X = df.drop('target', axis=1)
    y = df['target']

    # age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
    categorical_features = ['cp', 'restecg', 'slope', 'thal']
    numerical_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']
    pass_through_features = ['sex', 'fbs', 'exang']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('pass', 'passthrough', pass_through_features)
        ])

    # Deep Neural Network for "Acute" Risk
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', max_iter=500, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    print(f"Model UCI Accuracy: {model.score(X_test, y_test):.4f}")

    joblib.dump(model, 'model_uci.pkl')
    print("Saved model_uci.pkl")

if __name__ == "__main__":
    train_uci()
