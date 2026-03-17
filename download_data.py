import os
import sys

def check_data_exists(raw_data_path="data/raw"):
    """
    Checks if the Olist dataset files exist in the raw data directory.
    """
    required_files = [
        "olist_customers_dataset.csv",
        "olist_geolocation_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv",
        "olist_orders_dataset.csv",
        "olist_products_dataset.csv",
        "olist_sellers_dataset.csv",
        "product_category_name_translation.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(raw_data_path, file)):
            missing_files.append(file)
            
    return missing_files

def main():
    raw_path = os.path.join(os.getcwd(), "data", "raw")
    if not os.path.exists(raw_path):
        os.makedirs(raw_path)
        
    print(f"Checking for data in: {raw_path}")
    missing = check_data_exists(raw_path)
    
    if not missing:
        print("SUCCESS: All Olist dataset files found!")
    else:
        print("WARNING: The following files are missing:")
        for f in missing:
            print(f" - {f}")
        print("\nINSTRUCTIONS:")
        print("1. Go to https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
        print(f"2. Download the dataset and extract the CSV files into: {raw_path}")
        print("3. Alternatively, run 'python src/data/make_dataset.py' to generate synthetic data for testing.")

if __name__ == "__main__":
    main()
