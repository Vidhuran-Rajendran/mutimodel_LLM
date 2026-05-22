import camelot.io as camelot
import pandas as pd

def extract_pdf_tables(pdf_path):
    
    tables = camelot.read_pdf(pdf_path,pages ="all")
    dfs = []
    
    for i, table in enumerate(tables):
        df = table.df

        df.columns = df.iloc[0]
        df = df[1:]
        
        df.columns = [str(c).strip().lower() for c in df.columns]
        dfs.append(df)
    return dfs