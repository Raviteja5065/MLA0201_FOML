# Customer Churn Prediction and Segmentation System

An end-to-end Machine Learning project that predicts customer churn (**Churn vs. Non-Churn**) and performs customer segmentation using **K-Means Clustering** and **Principal Component Analysis (PCA)** on the public IBM Telco Customer Churn dataset.

---

## 📌 Project Overview

Customer retention is critical for subscription-based businesses like telecommunications. Acquiring a new customer costs 5 to 7 times more than retaining an existing subscriber. This repository provides a complete analytical pipeline that:
1. **Predicts Churn Probability**: Trains and evaluates four supervised machine learning models (**Logistic Regression**, **Naive Bayes**, **Decision Tree Classifier**, and **Random Forest Classifier**).
2. **Segments Customer Demographics**: Applies **K-Means Clustering** ($K=3$) to identify behavioral customer personas (**High-Risk**, **Medium-Risk**, **Loyal**).
3. **Visualizes High-Dimensional Clusters**: Uses **Principal Component Analysis (PCA)** to project feature spaces onto 2D scatter plots.
4. **Formulates Business Strategies**: Provides 5 data-backed customer retention recommendations.

---

## 📂 Project Directory Structure

```text
Customer-Churn-Prediction/
│
├── data/
│   └── Telco_Customer_Churn.csv        # IBM Telco Customer Churn Dataset (7,043 rows)
│
├── notebooks/
│   └── Customer_Churn_Prediction.ipynb  # Interactive Executable Jupyter Notebook
│
├── outputs/                            # Programmatically exported figures & artifacts
│   ├── churn_distribution.png
│   ├── gender_vs_churn.png
│   ├── contract_vs_churn.png
│   ├── monthly_charges_hist.png
│   ├── tenure_dist.png
│   ├── heatmap.png
│   ├── boxplot_monthly_charges.png
│   ├── confusion_matrix_lr.png
│   ├── confusion_matrix_nb.png
│   ├── confusion_matrix_dt.png
│   ├── confusion_matrix_rf.png
│   ├── accuracy_table.png
│   ├── elbow_method.png
│   ├── pca_clusters.png
│   └── final_prediction_output.png
│
├── README.md                           # Project Documentation
├── requirements.txt                    # Python Dependencies
├── main.py                             # Standalone Pipeline Execution Script
└── generate_report.py                  # DOCX Report Generator Script
```

---

## 📊 Dataset Information

* **Dataset Name**: IBM Telco Customer Churn Dataset
* **Source**: Kaggle Public Datasets
* **Sample Size**: 7,043 customer records
* **Total Features**: 21 columns (1 Target: `Churn`, 20 Features: Demographics, Services, Account details, Financial charges)
* **Preprocessing**: 
  - Median imputation for missing `TotalCharges` entries.
  - Identifier column `customerID` removed.
  - Categorical attributes encoded via One-Hot Encoding (`drop_first=True`).
  - Feature scaling using `StandardScaler`.

---

## 🤖 Model Performance Comparison

Evaluated on a 20% stratified test set ($N = 1,409$):

| Model | Accuracy | Precision | Recall | F1 Score | Evaluation Summary |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | **80.55%** | **65.72%** | **55.88%** | **60.40%** | ⭐ **Best Overall Balance** |
| **Random Forest** | **81.05%** | **68.90%** | 52.14% | 59.36% | Highest Accuracy & Precision |
| **Decision Tree Classifier** | 79.42% | 62.96% | 54.55% | 58.45% | Moderate Precision |
| **Naive Bayes (GaussianNB)** | 65.58% | 42.69% | **86.63%** | 57.19% | Highest Churn Recall |

---

## 💡 Customer Segments (K-Means & PCA)

Using K-Means ($K=3$), customers were partitioned into three distinct risk cohorts:
* 🔴 **Cluster 1: High-Risk Customers (46.34% Churn Rate)**: Short tenure (< 16 months), Month-to-month contracts, high monthly charges ($67.70), Fiber optic internet, Electronic check payments.
* 🟡 **Cluster 2: Medium-Risk Customers (12.66% Churn Rate)**: Long tenure (> 55 months), high monthly charges ($88.92), premium package subscribers.
* 🟢 **Cluster 0: Loyal Customers (7.40% Churn Rate)**: Moderate tenure (~30 months), basic service users, lowest monthly charges ($21.08).

---

## 🔑 Key Retention Recommendations

1. **Contract Migration Incentives**: Offer a 15% discount for Month-to-month subscribers upgrading to 1-year or 2-year contracts.
2. **Fiber Optic Support Bundling**: Bundle free online security and tech support for high-cost fiber optic customers.
3. **Auto-Pay Conversion Rebate**: Provide a $15 credit for electronic check users switching to credit card or bank auto-pay.
4. **90-Day Onboarding Support**: Deploy dedicated check-ins for new subscribers during their first 12 months.
5. **VIP Loyalty Renewal Perks**: Grant proactive renewal perks to long-tenure customers 60 days before contract expiry.

---

## ⚙️ Installation & Setup

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/your-username/Customer-Churn-Prediction.git
   cd Customer-Churn-Prediction
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Execution Instructions

### Option 1: Run the Pipeline via Python Script
To run preprocessing, training, evaluation, clustering, PCA, and figure generation in one command:
```bash
python main.py
```

### Option 2: Run via Jupyter Notebook
Launch Jupyter Notebook / VS Code and open `notebooks/Customer_Churn_Prediction.ipynb`:
```bash
jupyter notebook notebooks/Customer_Churn_Prediction.ipynb
```
