@echo off
echo ==========================================
echo AI-Driven Delivery Delay Risk Prediction
echo ==========================================

echo [0/5] Installing Dependencies...
pip install -r requirements.txt

echo [1/5] Generating Synthetic Data...
python src/data/make_dataset.py

echo [2/5] Cleaning Data...
python src/data/preprocess.py

echo [3/5] Engineering Features...
python src/features/build_features.py

echo [4/5] Generating Visualizations (EDA)...
python src/visualization/eda.py

echo [5/5] Training Models and Generating Report...
python src/models/train_model.py

echo.
echo ==========================================
echo EXECUTION COMPLETE!
echo ==========================================
echo.
echo 1. Check reports/figures/ for graphs.
echo 2. Check reports/model_performance.txt for accuracy.
echo 3. Check reports/PROJECT_REPORT.md for the final report.
echo.

echo [6/7] Launching Dashboard in 3 seconds...
timeout /t 3


python -m streamlit run src/app/app.py
pause
