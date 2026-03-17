import pandas as pd
import numpy as np
import os

def load_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_csv(filepath)

def clean_data(df):
    """
    Performs basic data cleaning steps.
    """
    # 1. Drop duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {initial_rows - len(df)} duplicate rows.")
    
    # 2. Handle Missing Values
    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("Missing values found:\n", missing[missing > 0])
        # Impute numerical with median
        num_cols = df.select_dtypes(include=['number']).columns
        for col in num_cols:
            df[col] = df[col].fillna(df[col].median())
        
        # Impute categorical with mode
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
             df[col] = df[col].fillna(df[col].mode()[0])
    
    # 3. Handle Outliers (Basic)
    # Ensure non-negative values for physical quantities
    cols_to_check = ['price', 'freight_value', 'distance_km', 'warehouse_processing_days']
    for col in cols_to_check:
        if col in df.columns:
            df = df[df[col] >= 0]
            
    # 4. Convert timestamps
    date_cols = ['order_purchase_timestamp', 'shipping_limit_date', 
                 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
            
    return df

def main():
    raw_path = os.path.join("data", "raw", "synthetic_delivery_data.csv")
    processed_path = os.path.join("data", "processed")
    
    if not os.path.exists(processed_path):
        os.makedirs(processed_path)
        
    try:
        print("Loading raw data...")
        df = load_data(raw_path)
        
        print("Cleaning data...")
        df_clean = clean_data(df)
        
        output_file = os.path.join(processed_path, "cleaned_data.csv")
        df_clean.to_csv(output_file, index=False)
        print(f"Cleaned data saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
