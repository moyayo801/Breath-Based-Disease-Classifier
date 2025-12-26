import pandas as pd
import numpy as np

def clean_libsvm_cell(cell):
    """
    Turns '123:0.527291' into 0.527291
    Turns NaN or empty into 0.0
    """
    if pd.isna(cell) or cell == "":
        return 0.0
    
    if isinstance(cell, str) and ":" in cell:
        try:
            return float(cell.split(":")[-1])
        except ValueError:
            return 0.0
    return cell

def fix_final_column(val):
    val_str = str(val)
    if ":" in val_str:
        return val_str.split(":")[0] 
    return val

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(script_dir, '..', 'data', 'raw', 'gas_data.csv')

print(f"Looking for file at: {data_path}")

try:
    df = pd.read_csv(data_path)
    print("Success! File loaded.")
except FileNotFoundError:
    print("Error: The file is still not there. Check if you ran your download script first!")

feature_cols = [col for col in df.columns if col != 'class']

print("Cleaning columns... this might take a second.")
for col in feature_cols:
    df[col] = df[col].apply(clean_libsvm_cell)

df['class'] = df['class'].apply(fix_final_column)

gas_names = {
    "1": "Ethanol",
    "2": "Ethylene",
    "3": "Ammonia",
    "4": "Acetaldehyde",
    "5": "Acetone",
    "6": "Toluene"
}
df['gas_name'] = df['class'].map(gas_names)

print("Clean-up complete!")
print(df.head())

if not os.path.exists('data/processed'):
    os.makedirs('data/processed')

df.to_csv('data/processed/gas_data_processed.csv', index=False)

print(f"File saved successfully at: processed/gas_data_processed.csv")