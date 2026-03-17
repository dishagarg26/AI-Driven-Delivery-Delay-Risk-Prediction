# Project Report: AI-Driven Delivery Delay Risk Prediction
## Amazon Supply Chain Intelligence

### 1. Executive Summary
This project presents an **AI-driven logistics intelligence system** designed to predict the risk of delivery delays in the Amazon India supply chain network. By leveraging machine learning models trained on synthetic operational data, the system classifies shipments as **On-Time**, **At Risk**, or **Delayed**. The solution includes a premium, Amazon-styled web dashboard for real-time risk assessment, order tracking, and performance analytics.

### 2. Problem Statement
Delivery delays significantly impact customer satisfaction and operational costs in e-commerce. Traditional routing systems often fail to account for dynamic factors such as:
-   **Traffic Congestion**: Unpredictable road conditions in major Indian cities.
-   **Weather Variability**: Impact of monsoons and storms on transit times.
-   **Peak Season Load**: Operational bottlenecks during festivals (e.g., Diwali).

**Goal**: Develop a predictive model to proactively identify high-risk shipments and enable preemptive intervention.

### 3. Solution Architecture
The system follows a modular data science pipeline:

1.  **Data Generation**:
    -   Synthetic dataset simulating **1,000+ orders** across major Indian cities (Mumbai, Delhi, Bangalore, etc.).
    -   Key Features: `price` (INR), `freight_value` (correlated with distance), `traffic_index` (confounded by weather), `delivery_speed`, and timestamps.
2.  **Data Preprocessing**:
    -   Cleaning: Handling missing values, outlier detection.
    -   Feature Engineering: `freight_ratio`, `is_peak_season`, `is_weekend`, `delivery_speed_km_h`.
    -   Encoding: Label encoding for categorical variables.
3.  **Model Development**:
    -   **Algorithms**: Logistic Regression, Random Forest, Gradient Boosting, XGBoost.
    -   **Imbalance Handling**: Synthetic Minority Over-sampling Technique (SMOTE).
    -   **Evaluation**: Accuracy, F1-Score, ROC-AUC, Confusion Matrix.
4.  **Deployment**:
    -   Interactive **Streamlit Dashboard** with "Amazon-style" premium UI.
    -   Real-time inference API.

### 4. Key Features
-   **Live Risk Prediction**: Input shipment details (Distance, Traffic, Weather) to get instant risk probability.
-   **Order Tracking**: Search for existing orders by ID (`ORD-XXXX`) to view their predicted status.
-   **Advanced Analytics**:
    -   **Feature Importance**: Identifies top drivers of delay (e.g., Traffic Index, Weather Severity).
    -   **ROC Curves**: Visualizes model sensitivity.
    -   **Model Comparison**: Benchmarks accuracy across different algorithms.

### 5. Technical Implementation
-   **Language**: Python 3.9+
-   **Libraries**:
    -   *Data Processing*: Pandas, NumPy
    -   *Machine Learning*: Scikit-learn, XGBoost, Imbalanced-learn (SMOTE)
    -   *Visualization*: Matplotlib, Seaborn
    -   *Web Framework*: Streamlit, Streamlit-Lottie (Animations)

### 6. Results & Analysis
*(See `reports/model_performance.txt` for specific metrics)*
-   **Top Performing Model**: Random Forest / Gradient Boosting (typically achieves >85% accuracy on synthetic data).
-   **Key Findings**:
    -   **Traffic Index** and **Weather Severity** are the strongest predictors of delay.
    -   **Peak Season** orders show a statistically significant increase in "At Risk" classifications.
    -   **Distance** alone is not a perfect predictor; `delivery_speed` (efficiency) matters more.

### 7. Future Scope
-   Integration with real-time API (Google Maps, OpenWeatherMap).
-   Route optimization suggestions for "At Risk" shipments.
-   Deployment to cloud (AWS/Azure) with CI/CD pipeline.
