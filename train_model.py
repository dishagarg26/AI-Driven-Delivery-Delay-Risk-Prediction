import pandas as pd
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
from itertools import cycle
from imblearn.over_sampling import SMOTE

try:
    import xgboost as xgb
except ImportError:
    print("XGBoost not installed, skipping.")
    xgb = None

def load_data(filepath):
    return pd.read_csv(filepath)

def train_models(X_train, y_train):
    # Handle Class Imbalance using SMOTE
    print("Applying SMOTE to handle class imbalance...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    print(f"Original shape: {X_train.shape}, Resampled shape: {X_train_resampled.shape}")

    models = {
        'LogisticRegression': LogisticRegression(max_iter=1000),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(random_state=42)
    }
    
    if xgb:
        models['XGBoost'] = xgb.XGBClassifier(random_state=42)
        
    trained_models = {}
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train_resampled, y_train_resampled)
        trained_models[name] = model
        
    return trained_models

def evaluate_models(models, X_test, y_test, output_dir):
    results = {}
    report_str = "Model Performance Report\n========================\n\n"
    
    for name, model in models.items():
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {acc:.4f}")
        results[name] = acc
        
        clf_report = classification_report(y_test, y_pred)
        report_str += f"Model: {name}\nAccuracy: {acc:.4f}\n{clf_report}\n\n"
        
        # Plot Confusion Matrix (Amazon Style)
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(7, 6))
        
        # Style
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['figure.facecolor'] = 'white'
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    cbar=False, linewidths=1, linecolor='white',
                    annot_kws={"size": 14, "weight": "bold"})
        
        plt.title(f'Confusion Matrix: {name}', fontsize=14, fontweight='bold', pad=15, color='#232F3E')
        plt.ylabel('Actual Class', fontsize=11, fontweight='bold')
        plt.xlabel('Predicted Class', fontsize=11, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'confusion_matrix_{name}.png'), dpi=300)
        plt.close()
        
        # Plot ROC Curve (Multiclass)
        # Binarize output
        y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
        n_classes = y_test_bin.shape[1]
        
        # Get probabilities
        try:
            if hasattr(model, "predict_proba"):
                y_score = model.predict_proba(X_test)
                
                # Compute ROC curve and ROC area for each class
                fpr = dict()
                tpr = dict()
                roc_auc = dict()
                for i in range(n_classes):
                    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
                    roc_auc[i] = auc(fpr[i], tpr[i])
                
                # Plot
                plt.figure(figsize=(8, 6))
                colors = cycle(['#232F3E', '#FF9900', '#146EB4']) # Navy, Orange, Blue -> At Risk, Delayed, On-Time
                class_names = ['At Risk', 'Delayed', 'On-Time']
                
                for i, color in zip(range(n_classes), colors):
                    plt.plot(fpr[i], tpr[i], color=color, lw=2,
                             label='ROC curve of class {0} (area = {1:0.2f})'.format(class_names[i], roc_auc[i]))
                
                plt.plot([0, 1], [0, 1], 'k--', lw=2)
                plt.xlim([0.0, 1.0])
                plt.ylim([0.0, 1.05])
                plt.xlabel('False Positive Rate', fontsize=12, fontweight='bold')
                plt.ylabel('True Positive Rate', fontsize=12, fontweight='bold')
                plt.title(f'ROC Curve: {name}', fontsize=14, fontweight='bold', pad=15, color='#232F3E')
                plt.legend(loc="lower right")
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, f'roc_curve_{name}.png'), dpi=300)
                plt.close()
        except:
            print(f"Skipping ROC for {name} (probability not supported)")
        
    # Save text report
    with open(os.path.join(output_dir, 'model_performance.txt'), 'w') as f:
        f.write(report_str)
    print(f"Performance report saved to {output_dir}/model_performance.txt")
    
    # Plot Model Comparison
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'sans-serif'
    
    names = list(results.keys())
    values = list(results.values())
    
    # Colors: Highlight best model
    best_idx = np.argmax(values)
    colors = ['#232F3E' if i != best_idx else '#FF9900' for i in range(len(names))]
    
    bars = plt.bar(names, values, color=colors, width=0.6)
    plt.ylim(0, 1.1)
    plt.title('Model Accuracy Comparison', fontsize=16, fontweight='bold', pad=20, color='#232F3E')
    plt.ylabel('Accuracy Score', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2%}',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
                 
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'model_comparison.png'), dpi=300)
    plt.close()
        
    return results

def plot_feature_importance(model, feature_names, output_dir):
    try:
        # Check if model has feature importances
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 8))
            plt.rcParams['font.family'] = 'sans-serif'
            
            sns.barplot(x=importances[indices], y=[feature_names[i] for i in indices], palette='Oranges_r')
            
            plt.title('Feature Importance (Top Factors)', fontsize=16, fontweight='bold', pad=20, color='#232F3E')
            plt.xlabel('Importance Score', fontsize=12)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'feature_importance.png'), dpi=300)
            plt.close()
            print("Feature importance plot saved.")
        else:
            print("Model does not support feature importance plotting.")
    except Exception as e:
        print(f"Error plotting feature importance: {e}")

def save_best_model(models, results, model_dir):
    best_name = max(results, key=results.get)
    best_model = models[best_name]
    print(f"Best Model: {best_name} with Accuracy: {results[best_name]:.4f}")
    
    with open(os.path.join(model_dir, 'best_model.pkl'), 'wb') as f:
        pickle.dump(best_model, f)
    print(f"Saved best model to {model_dir}/best_model.pkl")
    return best_model

def main():
    input_path = os.path.join("data", "processed", "final_data.csv")
    model_dir = os.path.join("models")
    report_dir = os.path.join("reports")
    figures_dir = os.path.join("reports", "figures")
    
    for d in [model_dir, report_dir, figures_dir]:
        if not os.path.exists(d):
            os.makedirs(d)
        
    if not os.path.exists(input_path):
        print("Data not found. Please run data processing scripts first.")
        return

    print("Loading data...")
    df = pd.read_csv(input_path)
    
    # Selecting features
    drop_cols = ['order_id', 'customer_id', 'order_purchase_timestamp', 
                 'shipping_limit_date', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date', 'delivery_status', 'seller_id',
                 # Drops to avoid leakage or mismatch
                 'delivery_days_actual', # LEAKAGE: We don't know this at inference time
                 'customer_city', 'customer_state', 'product_category', # Originals
                 'customer_city_encoded', 'customer_state_encoded', 'product_category_encoded' # Too high cardinality/complexity for simple demo app input
                 ]
    
    # Check for leakage
    feature_cols = [c for c in df.columns if c not in drop_cols and c != 'delivery_status_encoded']
    target_col = 'delivery_status_encoded'
    
    X = df[feature_cols]
    y = df[target_col]
    
    print(f"Training with {len(feature_cols)} features: {feature_cols}")
    
    # Save the feature names used for training to ensure app matches
    with open(os.path.join(model_dir, 'feature_names.pkl'), 'wb') as f:
        pickle.dump(feature_cols, f)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = train_models(X_train, y_train)
    results = evaluate_models(models, X_test, y_test, figures_dir)
    
    # Copy report to main report dir too
    import shutil
    shutil.copy(os.path.join(figures_dir, 'model_performance.txt'), os.path.join(report_dir, 'model_performance.txt'))
    
    best_model = save_best_model(models, results, model_dir)
    
    # Plot feature importance for best model
    plot_feature_importance(best_model, feature_cols, figures_dir)


if __name__ == "__main__":
    main()
