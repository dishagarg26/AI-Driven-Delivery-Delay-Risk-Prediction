import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. Amazon Branding & Style Setup ---
AMAZON_COLORS = {
    'primary': '#FF9900', # Orange (Delayed)
    'secondary': '#232F3E', # Dark Navy (At Risk)
    'accent': '#146EB4', # Blue (On-Time)
    'background': '#FFFFFF',
    'text': '#232F3E',
    'grid': '#E6E6E6'
}

# Color Mapping for Delivery Status
# 0: At Risk (Navy), 1: Delayed (Orange), 2: On-Time (Blue)
# Note: Label encoding order depends on alphabetical 'At Risk', 'Delayed', 'On-Time'
# A -> 0, D -> 1, O -> 2. So mapping is correct.
STATUS_COLORS = [AMAZON_COLORS['secondary'], AMAZON_COLORS['primary'], AMAZON_COLORS['accent']]

def set_style():
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['text.color'] = AMAZON_COLORS['text']
    plt.rcParams['axes.labelcolor'] = AMAZON_COLORS['text']
    plt.rcParams['xtick.color'] = AMAZON_COLORS['text']
    plt.rcParams['ytick.color'] = AMAZON_COLORS['text']
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['grid.color'] = AMAZON_COLORS['grid']
    plt.rcParams['axes.edgecolor'] = '#CCCCCC'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False

def plot_target_distribution(df, output_dir):
    set_style()
    plt.figure(figsize=(9, 6))
    
    # Count plot with custom colors
    # Ensure correct order if possible, but palette list works if sorted by value
    ax = sns.countplot(x='delivery_status', data=df, order=['At Risk', 'Delayed', 'On-Time'], palette=[AMAZON_COLORS['secondary'], AMAZON_COLORS['primary'], AMAZON_COLORS['accent']])
    
    plt.title('Distribution of Delivery Status', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Delivery Status', fontsize=12, fontweight='500')
    plt.ylabel('Number of Orders', fontsize=12, fontweight='500')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add labels on bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=11, color='#555', xytext=(0, 5), textcoords='offset points')
        
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'target_distribution.png'), dpi=300)
    plt.close()

def plot_correlation_matrix(df, output_dir):
    set_style()
    num_cols = df.select_dtypes(include=['number']).columns
    
    plt.figure(figsize=(12, 10))
    corr = df[num_cols].corr()
    
    # Mask upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Custom diverging palette
    cmap = sns.diverging_palette(240, 40, as_cmap=True) # Blue to Orange
    
    sns.heatmap(corr, mask=mask, annot=True, cmap=cmap, fmt=".2f", linewidths=1.0, 
                cbar_kws={"shrink": .8}, square=True, annot_kws={"size": 10})
                
    plt.title('Feature Correlation Matrix', fontsize=18, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'), dpi=300)
    plt.close()

def plot_boxplots(df, output_dir):
    set_style()
    
    # 1. Delivery Days Boxplot
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='delivery_status', y='delivery_days_actual', data=df, order=['At Risk', 'Delayed', 'On-Time'],
                palette=[AMAZON_COLORS['secondary'], AMAZON_COLORS['primary'], AMAZON_COLORS['accent']], 
                width=0.6, linewidth=1.5)
    plt.title('Delivery Duration vs Status', fontsize=15, fontweight='bold')
    plt.xlabel('Status')
    plt.ylabel('Actual Delivery Days')
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'delivery_days_boxplot.png'), dpi=300)
    plt.close()
    
    # 2. Traffic Impact Boxplot
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='delivery_status', y='traffic_index', data=df, order=['At Risk', 'Delayed', 'On-Time'],
                palette=[AMAZON_COLORS['secondary'], AMAZON_COLORS['primary'], AMAZON_COLORS['accent']], 
                width=0.6, linewidth=1.5)
    plt.title('Traffic Intensity vs Delivery Status', fontsize=15, fontweight='bold')
    plt.xlabel('Status')
    plt.ylabel('Traffic Index (0-10)')
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'traffic_impact_boxplot.png'), dpi=300)
    plt.close()

def main():
    input_path = os.path.join("data", "processed", "final_data.csv")
    output_dir = os.path.join("reports", "figures")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not os.path.exists(input_path):
        print("Final data not found. Run src/features/build_features.py first.")
        return

    print("Loading data for EDA...")
    df = pd.read_csv(input_path)
    
    print("Generating plots...")
    plot_target_distribution(df, output_dir)
    plot_correlation_matrix(df, output_dir)
    plot_boxplots(df, output_dir)
    
    print(f"EDA plots saved to: {output_dir}")

if __name__ == "__main__":
    main()
