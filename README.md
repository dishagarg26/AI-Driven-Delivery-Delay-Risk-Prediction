# AI-Driven Delivery Delay Risk Prediction

## Project Overview
This project builds an end-to-end machine learning system to predict delivery delay risks for e-commerce orders. It identifies key factors contributing to delays and classifies deliveries as **On-Time**, **At Risk**, or **Delayed**.

## Project Structure
```
├── data
│   ├── raw            # Original data (or synthetic)
│   └── processed      # Cleaned data for modeling
├── notebooks          # Jupyter notebooks for EDA and experiments
├── reports            # Generated analysis and figures
├── src
│   ├── app            # Streamlit dashboard
│   ├── data           # Data loading/generation scripts
│   ├── features       # Feature engineering
│   ├── models         # Model training scripts
│   └── visualization  # Plotting scripts
└── requirements.txt   # Python dependencies
```

## Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Data Acquisition**:
   - **Option A (Real Data)**: Download the [Olist E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place CSV files in `data/raw`.
   - **Option B (Synthetic Data)**: Run the generator script:
     ```bash
     python src/data/make_dataset.py
     ```

## Running the Dashboard
(Coming Soon)
```bash
streamlit run src/app/dashboard.py
```
