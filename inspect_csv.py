import pandas as pd
try:
    df = pd.read_csv('data_uci.csv')
    print("Columns found:", df.columns.tolist())
except Exception as e:
    print(f"Error reading CSV: {e}")
