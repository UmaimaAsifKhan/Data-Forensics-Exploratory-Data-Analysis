import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")

file_name = "Dataset for Data Analytics (1).xlsx"
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
file_path = os.path.join(downloads_path, file_name)

try:
    df = pd.read_excel(file_path)
    
    df = df.drop_duplicates()

    for col in df.select_dtypes(include=['object', 'string']).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace(['nan', 'None', '', 'null', 'nan'], 'Unknown')

    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce').fillna('Missing Date')

    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
        
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df[col] = np.clip(df[col], lower, upper)
        
        df[col] = df[col].round(2)

    output_path = os.path.join(downloads_path, "Cleaned_Data_Project2.csv")
    df.to_csv(output_path, index=False)
    
    print(" Forensic Process Complete. Cleaned data saved.")

except Exception as e:
    print(f" Error encountered: {e}")
