import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

def create_features(df):
    """
    Creates new features for the model.
    """
    # 1. Delivery Speed (km/day)
    # Avoid division by zero
    df['delivery_days_actual'] = df['delivery_days_actual'].replace(0, 0.1)
    df['delivery_speed_km_h'] = df['distance_km'] / (df['delivery_days_actual'] * 24) # km per hour approx
    
    # 2. Date components
    df['purchase_month'] = df['order_purchase_timestamp'].dt.month
    df['purchase_dow'] = df['order_purchase_timestamp'].dt.dayofweek
    df['purchase_hour'] = df['order_purchase_timestamp'].dt.hour
    
    # 3. Seasonality
    df['is_peak_season'] = df['purchase_month'].isin([10, 11, 12]).astype(int)
    
    # 4. Weekend Purchase
    df['is_weekend'] = df['purchase_dow'].isin([5, 6]).astype(int)
    
    # 5. Delay Risk Score (Proxy) - Ratio of Freight to Price (High freight might mean harder to ship)
    df['freight_ratio'] = df['freight_value'] / (df['price'] + 1)
    
    return df

def encode_features(df):
    """
    Encodes categorical variables.
    """
    le = LabelEncoder()
    cat_cols = ['customer_city', 'customer_state', 'product_category', 'delivery_status']
    
    encoders = {}
    for col in cat_cols:
        if col in df.columns:
            df[f'{col}_encoded'] = le.fit_transform(df[col])
            encoders[col] = le
            # Keep original for EDA, use encoded for model
            
    return df, encoders

def main():
    input_path = os.path.join("data", "processed", "cleaned_data.csv")
    output_path = os.path.join("data", "processed", "final_data.csv")
    
    if not os.path.exists(input_path):
        print("Cleaned data not found. Run src/data/preprocess.py first.")
        return

    print("Loading cleaned data...")
    df = pd.read_csv(input_path)
    
    # Re-parse dates because CSV loses datetime objects
    date_cols = ['order_purchase_timestamp', 'shipping_limit_date', 
                 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
            
    print("Engineering features...")
    df = create_features(df)
    
    print("Encoding features...")
    df, _ = encode_features(df)
    
    df.to_csv(output_path, index=False)
    print(f"Feature engineering complete. Saved to: {output_path}")
    print(f"Final shape: {df.shape}")

if __name__ == "__main__":
    main()
