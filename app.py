import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import requests
from streamlit_lottie import st_lottie
import time
from streamlit_folium import st_folium
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.map_utils import create_route_map, CITY_COORDS

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Amazon Prediction Delivery System",
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# --- 2. Custom CSS & Assets ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load Assets
lottie_logistics = load_lottieurl("https://lottie.host/1743a753-9111-4096-98ec-687865611099/z8L8v7wP9m.json") 
if not lottie_logistics:
    lottie_logistics = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_9wjm14ni.json")

# Premium Amazon-style CSS with High Contrast Sidebar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amazon+Ember:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Amazon Ember', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Global Background */
    .stApp {
        background: linear-gradient(180deg, #F2F4F8 0%, #E3E6EF 100%);
    }
    
    /* ------------------------------------------- */
    /*              SIDEBAR STYLING                */
    /* ------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #232F3E; /* Amazon Dark Blue */
        border-right: 1px solid #37475A;
    }
    
    /* Sidebar Text Color Fix - FORCE WHITE */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }
    
    /* Sidebar Inputs */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div {
        background-color: #FF9900 !important; /* Slider orange */
    }
    section[data-testid="stSidebar"] .stSlider > div > div > div > div[role="slider"] {
        box-shadow: 0 0 10px rgba(255, 153, 0, 0.5);
    }
    
    /* Expander Styling in Sidebar */
    section[data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #37475A;
        color: white;
        border-radius: 5px;
        margin-bottom: 5px;
    }
    section[data-testid="stSidebar"] .streamlit-expanderContent {
        background-color: #232F3E;
        color: white !important;
        border: 1px solid #37475A;
    }

    /* ------------------------------------------- */
    /*              MAIN DASHBOARD                 */
    /* ------------------------------------------- */
    
    /* Hero Title */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #232F3E;
        background: -webkit-linear-gradient(45deg, #232F3E, #37475A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #FF9900;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); /* Soft Shadow */
        border-top: 4px solid #FF9900;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.8s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    /* Animations */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Primary Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #FF9900 0%, #FFB84D 100%);
        color: #111;
        border: none;
        padding: 15px 32px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(255, 153, 0, 0.4);
        width: 100%;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 8px 25px rgba(255, 153, 0, 0.6);
        color: white;
    }
    
    /* Divider */
    hr {
        margin: 30px 0;
        border: 0;
        border-top: 1px solid #E3E6EF;
    }
    
    </style>
""", unsafe_allow_html=True)

# --- 3. Model Loading & Utils ---
@st.cache_resource
def load_assets():
    model_path = os.path.join("models", "best_model.pkl")
    # Load Model
    model = None
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    return model

model = load_assets()

# --- 4. Sidebar ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=160)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    st.markdown("### 🛠 CONTROL PANEL")
    
    with st.expander("📦 SHIPMENT PARAMETERS", expanded=True):
        distance = st.slider("Distance (km)", 10, 3000, 500)
        warehouse_days = st.slider("Warehouse Prep (Days)", 0, 5, 1)
        freight = st.number_input("Freight Cost (₹)", 50.0, 5000.0, 150.0)
    
    with st.expander("🌦 EXTERNAL CONDITIONS", expanded=True):
        weather = st.slider("Weather Severity (0-10)", 0.0, 10.0, 2.0)
        traffic = st.slider("Traffic Level (0-10)", 0.0, 10.0, 4.0)

    with st.expander("📑 ORDER DETAILS"):
        price = st.number_input("Order Value (₹)", 100.0, 500000.0, 1500.0)
        is_peak = st.checkbox("Peak Season", False)
        is_weekend = st.checkbox("Weekend Delivery", False)
    
    st.markdown("---")
    st.caption("AI Model v2.3 • Amazon Internal Tools")

# --- 5. Main Content ---

# HERO SECTION
c1, c2 = st.columns([1, 4])
with c1:
    if lottie_logistics:
        st_lottie(lottie_logistics, height=180, key="hero_anim")
    else:
        st.image("https://img.icons8.com/color/144/000000/drone-delivery.png")

with c2:
    st.markdown('<div class="hero-title">Amazon Prediction Delivery System</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Amazon Supply Chain Intelligence</div>', unsafe_allow_html=True)
    st.markdown("*Advanced AI-driven analytics for predicting shipment risks in real-time.*")

st.markdown("---")

# Navigation Tabs
tabs = st.tabs(["⚡ LIVE PREDICTION", "🔍 TRACK ORDER", "📈 ANALYTICS DEEP DIVE", "🗺️ ROUTE OPTIMIZATION"])

# --- TAB 1: LIVE PREDICTION ---
with tabs[0]:
    # METRICS ROW
    st.markdown("### 📊 Active Shipment Overview")
    k1, k2, k3, k4 = st.columns(4)
    
    def metric_card(title, value, desc, color="#FF9900"):
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {color};">
            <h4 style="margin:0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color:#555;">{title}</h4>
            <h2 style="margin:10px 0; color:#232F3E; font-size: 28px;">{value}</h2>
            <p style="margin:0; font-size:13px; color:#777;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with k1: metric_card("Distance", f"{distance} km", "Intra-State Route", "#232F3E")
    with k2: metric_card("Order Value", f"₹ {price:,.0f}", f"Freight: {freight/price:.1%}", "#FF9900")
    with k3: metric_card("Traffic Density", f"{traffic}/10", "Moderate Congestion", "#17A2B8")
    with k4: metric_card("Weather Risk", f"{weather}/10", "Stormy Conditions" if weather > 6 else "Safe Fly Zone", "#DC3545" if weather > 6 else "#28A745")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Eng Calculation for Model Input
    target_days = 4
    speed_km_h = distance / (target_days * 24)
    freight_ratio = freight / (price + 0.1)
    
    input_data = pd.DataFrame({
        'price': [price],
        'freight_value': [freight],
        'warehouse_processing_days': [warehouse_days],
        'distance_km': [distance],
        'traffic_index': [traffic],
        'weather_severity': [weather],
        'delivery_speed_km_h': [speed_km_h],
        'purchase_month': [6], 
        'purchase_dow': [2], 
        'purchase_hour': [14], 
        'is_peak_season': [int(is_peak)],
        'is_weekend': [int(is_weekend)],
        'freight_ratio': [freight_ratio]
    })
    
    # Predict Button area
    c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
    with c_btn2:
        predict_clicked = st.button("🚀 PREDICT DELIVERY RISK", key="live_btn")

    if predict_clicked:
        if model:
            with st.spinner("Analyzing Supply Chain Neural Network..."):
                time.sleep(1.2) # Animation delay
                
                try:
                    prediction = model.predict(input_data)
                    probs = model.predict_proba(input_data)
                    
                    status_map = {0: "At Risk", 1: "Delayed", 2: "On-Time"}
                    result = status_map.get(prediction[0], "Unknown")
                    
                    # RESULT DISPLAY
                    st.markdown("---")
                    r1, r2 = st.columns([1, 1])
                    
                    with r1:
                        st.markdown(f"### 🎯 Forecast: **{result}**")
                        if result == "On-Time":
                            st.success("✅ Shipment is operating within optimal parameters.")
                            st.balloons()
                        elif result == "At Risk":
                            st.warning("⚠️ Elevated risk detected. Monitor closely.")
                        else:
                            st.error("🚨 Critical Delay Detected. Intervention recommended.")
                            
                        # Recommendation
                        st.info("💡 **AI Strategy**: " + 
                                ("Continue standard routing." if result=="On-Time" else 
                                 "Consider expedited freight upgrade." if result=="At Risk" else 
                                 "Notify CX team and reroute via priority lane."))

                    with r2:
                        st.markdown("### 📉 Confidence Levels")
                        # Detailed Bars
                        st.caption("At Risk Probability")
                        st.progress(float(probs[0][0]))
                        st.caption("Delayed Probability")
                        st.progress(float(probs[0][1]))
                        st.caption("On-Time Probability")
                        st.progress(float(probs[0][2]))

                except Exception as e:
                    st.error(f"Prediction Error: {e}")
                    st.warning("Please ensure feature inputs match the trained model.")
        else:
            st.error("⚠️ Model not found. Run 'run_project.bat' first.")

# --- TAB 2: TRACK ORDER ---
with tabs[1]:
    st.markdown("### 🔎 Track & Trace")
    c_search1, c_search2 = st.columns([3,1])
    with c_search1:
        search_query = st.text_input("Order / Customer ID", placeholder="Ex: ORD-00432")
    with c_search2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        search_click = st.button("Search Database", key="track_btn")
    
    if search_click:
        data_path = os.path.join("data", "raw", "synthetic_delivery_data.csv")
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            res = df[(df['order_id'] == search_query) | (df['customer_id'] == search_query)]
            
            if not res.empty:
                row = res.iloc[0]
                
                # Info Display
                st.success(f"✅ Order Found: **{row['order_id']}**")
                
                info1, info2, info3 = st.columns(3)
                info1.metric("Origin City", row['customer_city'])
                info2.metric("SKU Category", row['product_category'])
                info3.metric("Purchase Date", row['order_purchase_timestamp'][:10])
                
                # Auto-Predict for this order
                if model:
                    # Construct matching input
                    o_price = row['price']
                    o_freight = row['freight_value']
                    o_dist = row['distance_km']
                    o_traffic = row['traffic_index']
                    o_weather = row['weather_severity']
                    
                    # Calc
                    o_speed = o_dist / (4 * 24)
                    
                    track_input = pd.DataFrame({
                        'price': [o_price], 'freight_value': [o_freight],
                        'warehouse_processing_days': [row['warehouse_processing_days']],
                        'distance_km': [o_dist], 'traffic_index': [o_traffic],
                        'weather_severity': [o_weather], 'delivery_speed_km_h': [o_speed],
                        'purchase_month': [6], 'purchase_dow': [2], 'purchase_hour': [14], # Defaults
                        'is_peak_season': [0], 'is_weekend': [0],
                        'freight_ratio': [o_freight / (o_price + 0.1)]
                    })
                    
                    pred_t = model.predict(track_input)
                    status_map = {0: "At Risk", 1: "Delayed", 2: "On-Time"}
                    res_t = status_map.get(pred_t[0], "Unknown")
                    
                    st.markdown(f"#### AI Status Prediction: :{('green' if res_t=='On-Time' else 'red')}[{res_t}]")
            else:
                st.error("❌ Order ID not found.")
        else:
            st.error("Database unavailable.")

# --- TAB 3: ANALYTICS ---
with tabs[2]:
    st.markdown("### 📈 Performance Analytics")
    
    figures_dir = os.path.join("reports", "figures")
    
    # Row 1: Model Comparison & Feature Importance
    c_perf1, c_perf2 = st.columns(2)
    
    with c_perf1:
        st.markdown("#### 🏆 Model Comparison")
        if os.path.exists(os.path.join(figures_dir, "model_comparison.png")):
            st.image(os.path.join(figures_dir, "model_comparison.png"), use_column_width=True, caption="Accuracy Scores per Model")
        else:
            st.info("Run training to view comparison.")

    with c_perf2:
        st.markdown("#### 🔑 Key Risk Factors (Feature Importance)")
        if os.path.exists(os.path.join(figures_dir, "feature_importance.png")):
            st.image(os.path.join(figures_dir, "feature_importance.png"), use_column_width=True, caption="Top Drivers of Delivery Risk")
        else:
            st.info("Feature importance not available.")

    st.markdown("---")
    
    # Row 2: ROC Curves & Confusion Matrix
    st.markdown("#### 🎯 Model Sensitivity Analysis (ROC Curves)")
    
    roc1, roc2, roc3 = st.columns(3)
    if os.path.exists(os.path.join(figures_dir, "roc_curve_RandomForest.png")):
        roc1.image(os.path.join(figures_dir, "roc_curve_RandomForest.png"), caption="ROC - Random Forest")
    if os.path.exists(os.path.join(figures_dir, "roc_curve_LogisticRegression.png")):
        roc2.image(os.path.join(figures_dir, "roc_curve_LogisticRegression.png"), caption="ROC - Logistic Regression")
    if os.path.exists(os.path.join(figures_dir, "roc_curve_GradientBoosting.png")):
        roc3.image(os.path.join(figures_dir, "roc_curve_GradientBoosting.png"), caption="ROC - Gradient Boosting")
        
    st.markdown("---")
    
    # Row 3: EDA
    st.markdown("#### 🔍 Exploratory Data Analysis")
    a1, a2 = st.columns(2)
    
    with a1:
        st.markdown("**Feature Correlations**")
        if os.path.exists(os.path.join(figures_dir, "correlation_matrix.png")):
            st.image(os.path.join(figures_dir, "correlation_matrix.png"), use_column_width=True)
            
    with a2:
        st.markdown("**Target Class Distribution**")
        if os.path.exists(os.path.join(figures_dir, "target_distribution.png")):
            st.image(os.path.join(figures_dir, "target_distribution.png"), use_column_width=True)

    st.markdown("---")
    
    # Row 4: Confusion Matrices
    st.markdown("#### 📉 Model Performance (Confusion Matrix)")
    
    cm1, cm2, cm3 = st.columns(3)
    if os.path.exists(os.path.join(figures_dir, "confusion_matrix_RandomForest.png")):
        cm1.image(os.path.join(figures_dir, "confusion_matrix_RandomForest.png"), caption="Random Forest")
    if os.path.exists(os.path.join(figures_dir, "confusion_matrix_LogisticRegression.png")):
        cm2.image(os.path.join(figures_dir, "confusion_matrix_LogisticRegression.png"), caption="Logistic Regression")
    if os.path.exists(os.path.join(figures_dir, "confusion_matrix_GradientBoosting.png")):
        cm3.image(os.path.join(figures_dir, "confusion_matrix_GradientBoosting.png"), caption="Gradient Boosting")

# --- TAB 4: ROUTE OPTIMIZATION ---
with tabs[3]:
    st.markdown("### 🗺️ Intelligent Route Optimization")
    st.markdown("Visualize the predicted delivery path and identify high-risk traffic zones.")
    
    col_map1, col_map2 = st.columns([1, 2])
    
    with col_map1:
        st.markdown("#### Configure Route")
        
        # City selection
        city_list = list(CITY_COORDS.keys())
        source = st.selectbox("📍 Origin", city_list, index=0)
        destination = st.selectbox("🏁 Destination", city_list, index=1)
        
        if source == destination:
            st.warning("Source and Destination cannot be the same.")
            
        # Simulate conditions for visualization
        sim_traffic = st.slider("Traffic Density (Simulation)", 0, 10, 5)
        sim_weather = st.slider("Weather Severity (Simulation)", 0, 10, 2)
        
        # Calculate Dummy Risk based on simulation (or use real model if inputs mapped)
        # Simple heuristic for visual demo:
        risk_score = 0
        if sim_traffic > 7 or sim_weather > 7:
            risk_score = 2 # High
        elif sim_traffic > 4:
            risk_score = 1 # Medium
        
        st.info(f"Predicted Risk Level: **{['Low', 'Medium', 'High'][risk_score]}**")
        
    with col_map2:
        st.markdown("#### 🛰️ Live Route Map")
        if source != destination:
            map_obj = create_route_map(source, destination, risk_score)
            st_folium(map_obj, width=700, height=500)





# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #777; font-size: 12px;'>© 2026 Amazon Supply Chain Solutions | Confidential & Proprietary</div>", unsafe_allow_html=True)
