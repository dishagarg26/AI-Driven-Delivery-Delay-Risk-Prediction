from fpdf import FPDF
import os
import datetime

class PDFReport(FPDF):
    def header(self):
        # Logo
        # self.image('logo.png', 10, 8, 33) 
        self.set_font('Arial', 'B', 20)
        self.set_text_color(35, 47, 62) # Amazon Navy
        self.cell(0, 10, 'Amazon Supply Chain Intelligence', 0, 1, 'C')
        self.set_font('Arial', 'I', 12)
        self.set_text_color(255, 153, 0) # Amazon Orange
        self.cell(0, 10, 'AI-Driven Delivery Delay Risk Prediction Report', 0, 1, 'C')
        self.ln(5)
        self.line(10, 35, 200, 35)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb} | Generated on ' + datetime.datetime.now().strftime("%Y-%m-%d"), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(35, 47, 62)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_image(self, image_path, caption):
        if os.path.exists(image_path):
            self.ln(5)
            # Center image roughly
            self.image(image_path, x=25, w=160)
            self.ln(2)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 5, caption, 0, 1, 'C')
            self.ln(10)
        else:
            self.set_font('Arial', 'I', 10)
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, f"Image not found: {os.path.basename(image_path)}", 0, 1, 'C')

def generate_pdf():
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # 1. Executive Summary
    pdf.chapter_title('1. Executive Summary')
    pdf.chapter_body(
        "This report details the performance and insights of the AI-driven delivery risk prediction system. "
        "The system utilizes advanced machine learning algorithms to predict whether a shipment "
        "will be On-Time, At Risk, or Delayed based on operational factors like traffic, weather, and distance."
    )
    
    # 2. Key Insights from Data (EDA)
    pdf.chapter_title('2. Exploratory Data Analysis (EDA)')
    pdf.chapter_body(
        "Before training, we analyzed the dataset to understand key drivers of delay. "
        "The following visualizations highlight the relationships between variables."
    )
    
    figures_dir = os.path.join("reports", "figures")
    
    pdf.add_image(os.path.join(figures_dir, 'target_distribution.png'), "Fig 1: Distribution of Delivery Status Classes")
    pdf.chapter_body(
        "This chart shows the balance of our training data. We used SMOTE (Synthetic Minority Over-sampling Technique) "
        "to ensure the model doesn't become biased towards the majority class."
    )
    
    pdf.add_image(os.path.join(figures_dir, 'correlation_matrix.png'), "Fig 2: Feature Correlation Matrix")
    pdf.chapter_body(
        "The correlation matrix reveals strong dependencies. "
        "Traffic Index and Weather Severity show positive correlation with delays."
    )
    
    pdf.add_page()
    pdf.chapter_title('3. Model Performance')
    pdf.chapter_body(
        "We trained and evaluated multiple models: Logistic Regression, Random Forest, and Gradient Boosting. "
        "Below is the accuracy comparison and detailed sensitivity analysis."
    )
    
    pdf.add_image(os.path.join(figures_dir, 'model_comparison.png'), "Fig 3: Model Accuracy Benchmark")
    
    # Read performance text
    metrics_path = os.path.join("reports", "model_performance.txt")
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            metrics_text = f.read()
        pdf.set_font("Courier", size=9)
        pdf.multi_cell(0, 5, metrics_text)
        pdf.ln()

    pdf.add_page()
    pdf.chapter_title('4. Detailed Evaluation (Confusion Matrices)')
    pdf.chapter_body("Confusion matrices help us understand where the model makes mistakes.")
    
    pdf.add_image(os.path.join(figures_dir, 'confusion_matrix_RandomForest.png'), "Fig 4: Random Forest Confusion Matrix")
    pdf.add_image(os.path.join(figures_dir, 'confusion_matrix_GradientBoosting.png'), "Fig 5: Gradient Boosting Confusion Matrix")

    pdf.add_page()
    pdf.chapter_title('5. ROC Curves (Sensitivity Analysis)')
    pdf.chapter_body("ROC Curves demonstrate the model's ability to distinguish between classes at different thresholds.")
    
    pdf.add_image(os.path.join(figures_dir, 'roc_curve_RandomForest.png'), "Fig 6: ROC Curve - Random Forest")
    pdf.add_image(os.path.join(figures_dir, 'roc_curve_GradientBoosting.png'), "Fig 7: ROC Curve - Gradient Boosting")

    pdf.add_page()
    pdf.chapter_title('6. Business Impact & Feature Importance')
    pdf.chapter_body(
        "Understanding which factors contribute most to risk is crucial for operational decision-making. "
        "The chart below identifies the top drivers of delivery risk."
    )
    pdf.add_image(os.path.join(figures_dir, 'feature_importance.png'), "Fig 8: Feature Importance (Key Drivers)")
    
    pdf.chapter_body(
        "Recommendations:\n"
        "- Prioritize 'At Risk' shipments for expedited routing.\n"
        "- Monitor weather forecasts closely as they strongly confound traffic delays.\n"
        "- Use this model to proactively notify customers of potential delays."
    )

    # Output
    output_path = os.path.join("reports", "Final_Project_Report.pdf")
    pdf.output(output_path, 'F')
    print(f"PDF Report generated successfully: {output_path}")

if __name__ == "__main__":
    generate_pdf()
