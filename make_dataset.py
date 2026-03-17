import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(n_samples=1000, output_path="data/raw"):
    """
    Generates a synthetic logistics dataset for development and testing.
    Mimics the structure needed for the delivery delay risk prediction.
    """
    print(f"Generating {n_samples} synthetic records...")
    
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime(2024, 1, 1) # Updated to 2024
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_samples)]
    
    # Generate features (Indian Context)
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
    states = ['MH', 'DL', 'KA', 'TG', 'TN', 'WB', 'MH', 'GJ', 'RJ', 'UP']
    
    # Map city to state roughly for realism (simplified)
    city_state_map = dict(zip(cities, states))
    random_cities = np.random.choice(cities, n_samples)
    random_states = [city_state_map[c] for c in random_cities]
    
    # Generate Correlated Features
    # 1. Distance (random)
    distances = np.random.randint(10, 3000, n_samples)
    
    # 2. Freight (depends on distance + noise)
    # Base 50 + 0.1 per km + random variation
    freight = 50 + (distances * 0.1) + np.random.normal(0, 20, n_samples)
    freight = np.clip(freight, 50, 5000) # Ensure valid range
    
    # 3. Weather (random)
    weather = np.random.uniform(0, 10, n_samples)
    
    # 4. Traffic (confounded by weather: bad weather -> worse traffic)
    # Base random + 0.3 * weather
    traffic = np.random.uniform(0, 7, n_samples) + (0.3 * weather)
    traffic = np.clip(traffic, 0, 10)
    
    data = {
        'order_id': [f'ORD-{i:05d}' for i in range(n_samples)],
        'customer_id': [f'CUST-{np.random.randint(1000, 9999)}' for _ in range(n_samples)],
        'order_purchase_timestamp': dates,
        'customer_city': random_cities,
        'customer_state': random_states,
        'product_category': np.random.choice(['electronics', 'fashion', 'home_decor', 'health_beauty', 'sports', 'books', 'grocery'], n_samples),
        'price': np.round(np.random.uniform(500, 50000, n_samples), 2), # INR Range
        'freight_value': np.round(freight, 2), # Correlated
        'warehouse_processing_days': np.random.randint(0, 5, n_samples),
        'distance_km': distances,
        'traffic_index': np.round(traffic, 1), # Correlated
        'weather_severity': np.round(weather, 1),
        'seller_id': [f'SELLER-{np.random.randint(100, 999)}' for _ in range(n_samples)],
        'shipping_limit_date': [d + timedelta(days=np.random.randint(2, 5)) for d in dates],
    }
    
    df = pd.DataFrame(data)
    
    # Simulate delivery process
    # Warehouse processing time (0-3 days)
    df['warehouse_processing_days'] = np.random.randint(0, 4, n_samples)
    
    # Distance (simulated)
    df['distance_km'] = np.random.uniform(10, 1000, n_samples)
    
    # Traffic/Weather factors (random scores 0-10)
    df['traffic_index'] = np.random.uniform(0, 10, n_samples)
    df['weather_severity'] = np.random.uniform(0, 10, n_samples)
    
    # Calculate delivery time based on distance + random variance + delays
    # Base: 50km/day
    base_days = df['distance_km'] / 200 # faster delivery
    noise = np.random.normal(1, 0.5, n_samples)
    delay_factors = (df['traffic_index'] * 0.1) + (df['weather_severity'] * 0.15)
    
    total_days = base_days + noise + delay_factors + df['warehouse_processing_days']
    total_days = np.clip(total_days, 1, 30) # Minimum 1 day
    
    df['delivery_days_actual'] = np.round(total_days, 1)
    df['order_delivered_customer_date'] = df['order_purchase_timestamp'] + pd.to_timedelta(df['delivery_days_actual'], unit='D')
    
    # Estimated delivery date (Target expectation)
    # Estimate is usually actual - delay or just a standard calculation
    # Let's say estimate was distance/200 + 2 days buffer
    df['order_estimated_delivery_date'] = df['order_purchase_timestamp'] + pd.to_timedelta((df['distance_km'] / 200) + 3, unit='D')
    
    # Create Target Variable
    # On-Time: Delivered <= Estimated
    # At Risk: Delivered > Estimated but < Estimated + 2 days
    # Delayed: Delivered > Estimated + 2 days
    
    def classify_status(row):
        actual = row['order_delivered_customer_date']
        estimated = row['order_estimated_delivery_date']
        
        if actual <= estimated:
            return 'On-Time'
        elif actual <= estimated + timedelta(days=2):
            return 'At Risk'
        else:
            return 'Delayed'

    df['delivery_status'] = df.apply(classify_status, axis=1)
    
    # Save
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    output_file = os.path.join(output_path, "synthetic_delivery_data.csv")
    df.to_csv(output_file, index=False)
    print(f"Synthetic data saved to: {output_file}")
    
    # Also save a version that looks like Olist orders for compatibility if we want to get fancy later
    # For now, this consolidated dataset is easier for the user to start with.

if __name__ == "__main__":
    generate_synthetic_data()
