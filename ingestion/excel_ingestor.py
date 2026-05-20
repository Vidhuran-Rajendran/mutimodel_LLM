import pandas as pd

def load_excel(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    df.columns = df.columns.str.strip().str.lower()
    return df