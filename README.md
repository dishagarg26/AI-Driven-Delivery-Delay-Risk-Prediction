# AI-Driven Delivery Delay Risk Prediction

## Project Overview
This project is an end-to-end machine learning solution that predicts delivery delay risk for e-commerce orders. It classifies each delivery into one of three categories:

✅ On-Time – Delivery is predicted to arrive on schedule
⚠️ At Risk – Delivery is flagged as likely to be delayed
❌ Delayed – Delivery is predicted to arrive late
The system identifies key factors that influence delivery delays and supports proactive mitigation, enabling smarter decision-making across supply chain and logistics operations.

## 🧩 Key Value Proposition
Proactive risk detection: Flag orders that are likely to be delayed before they happen
Root cause insight: Identify which features (e.g., weather, distance, carrier performance) drive delay risk
Scalable workflow: Works with synthetic datasets or real e-commerce order data
Easy to integrate: Model and dashboard code is packaged for deployment and analysis

## Project Structure
```
├── data
│   ├── raw            # Raw input CSVs (real or synthetic)
│   └── processed      # Cleaned, feature-ready datasets
├── models             # Trained model artifacts / checkpoints
├── reports            # Analysis outputs & model performance reports
├── src
│   ├── app            # Streamlit dashboard (visualization + user interface)
│   ├── data           # Data generation + preprocessing scripts
│   ├── features       # Feature engineering logic
│   ├── models         # Training and evaluation scripts
│   └── visualization  # Plotting / report generation scripts
└── requirements.txt   # Python dependencies
```

## Benefits to a Business / Team
Reduced delivery risk by predicting delays early
Improved customer satisfaction via proactive notifications
Operational efficiency by flagging orders needing intervention
Data-driven insight into root causes of delivery slippage

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

