import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Set style for professional graphs
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.family': 'sans-serif'})

def main():
    print("=" * 70)
    print("Customer Churn Prediction and Segmentation System (ML Project)")
    print("=" * 70)

    # Create directories if not exist
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    # 1. Load Dataset
    data_path = 'data/Telco_Customer_Churn.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df_raw = pd.read_csv(data_path)
    print(f"\n[1] Dataset Loaded Successfully! Source: IBM Telco Churn Dataset")
    print(f"Dataset Shape: {df_raw.shape} (Rows: {df_raw.shape[0]}, Columns: {df_raw.shape[1]})")
    print("\nInitial Missing Values Per Column:\n", df_raw.isnull().sum())

    # 2. Data Preprocessing
    df = df_raw.copy()

    # Step 1: Convert TotalCharges to numeric FIRST before categorical detection
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(' ', np.nan), errors='coerce')
    missing_tc = df['TotalCharges'].isnull().sum()
    print(f"\nFound {missing_tc} missing values in TotalCharges. Imputing with median TotalCharges...")
    df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

    # Step 2: Remove CustomerID
    if 'customerID' in df.columns:
        df_processed = df.drop(columns=['customerID'])
    else:
        df_processed = df.copy()

    # Step 3: Identify categorical and numeric columns
    cat_cols = df_processed.select_dtypes(include=['object', 'string']).columns.tolist()
    if 'Churn' in cat_cols:
        cat_cols.remove('Churn')

    # Step 4: Map target Churn to binary 1/0
    df_processed['Churn_Numeric'] = df_processed['Churn'].map({'Yes': 1, 'No': 0})

    # Step 5: One-Hot Encoding for multi-categorical variables
    df_encoded = pd.get_dummies(df_processed, columns=cat_cols, drop_first=True)
    df_encoded['Churn'] = df_processed['Churn_Numeric']
    df_encoded = df_encoded.drop(columns=['Churn_Numeric'])

    print(f"\nDataset After Preprocessing & One-Hot Encoding: Shape: {df_encoded.shape}")

    # Save clean copy reference
    df_clean = df_processed.copy()

    # 3. Exploratory Data Analysis (EDA) & Visualization Exports
    print("\n[3] Generating EDA Visualizations...")

    # 1) Churn distribution bar chart
    plt.figure(figsize=(7, 5))
    ax = sns.countplot(x='Churn', data=df_clean, palette=['#2ca02c', '#d62728'], hue='Churn', legend=False)
    plt.title('Customer Churn Distribution', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Churn Status', fontsize=12)
    plt.ylabel('Customer Count', fontsize=12)
    total = len(df_clean)
    for p in ax.patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        x = p.get_x() + p.get_width() / 2 - 0.1
        y = p.get_height() + 50
        ax.annotate(f'{p.get_height()}\n({percentage})', (x, y), ha='center', fontsize=10)
    plt.tight_layout()
    plt.savefig('outputs/churn_distribution.png', dpi=300)
    plt.close()

    # 2) Gender vs Churn
    plt.figure(figsize=(7, 5))
    sns.countplot(x='gender', hue='Churn', data=df_clean, palette=['#1f77b4', '#ff7f0e'])
    plt.title('Churn Rate by Gender', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Gender', fontsize=12)
    plt.ylabel('Customer Count', fontsize=12)
    plt.legend(title='Churn', frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/gender_vs_churn.png', dpi=300)
    plt.close()

    # 3) Contract Type vs Churn
    plt.figure(figsize=(8, 5))
    sns.countplot(x='Contract', hue='Churn', data=df_clean, palette=['#2b5c8f', '#d9534f'])
    plt.title('Churn Rate by Contract Type', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Contract Type', fontsize=12)
    plt.ylabel('Customer Count', fontsize=12)
    plt.legend(title='Churn', frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/contract_vs_churn.png', dpi=300)
    plt.close()

    # 4) Monthly Charges histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df_clean, x='MonthlyCharges', hue='Churn', kde=True, element="step", palette=['#2ca02c', '#d62728'])
    plt.title('Monthly Charges Distribution by Churn Status', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Monthly Charges ($)', fontsize=12)
    plt.ylabel('Customer Count', fontsize=12)
    plt.tight_layout()
    plt.savefig('outputs/monthly_charges_hist.png', dpi=300)
    plt.close()

    # 5) Tenure distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df_clean, x='tenure', hue='Churn', kde=True, bins=30, palette=['#1f77b4', '#e377c2'])
    plt.title('Customer Tenure Distribution (Months)', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Tenure (Months)', fontsize=12)
    plt.ylabel('Customer Count', fontsize=12)
    plt.tight_layout()
    plt.savefig('outputs/tenure_dist.png', dpi=300)
    plt.close()

    # 6) Correlation heatmap
    plt.figure(figsize=(10, 8))
    corr_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn', 
                 'Contract_One year', 'Contract_Two year', 
                 'InternetService_Fiber optic', 'PaymentMethod_Electronic check', 
                 'PaperlessBilling_Yes', 'SeniorCitizen']
    corr_matrix = df_encoded[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, cbar=True)
    plt.title('Feature Correlation Heatmap with Churn', fontsize=14, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig('outputs/heatmap.png', dpi=300)
    plt.close()

    # 7) Boxplot of Monthly Charges vs Churn
    plt.figure(figsize=(7, 5))
    sns.boxplot(x='Churn', y='MonthlyCharges', data=df_clean, palette=['#5b9bd5', '#ed7d31'], hue='Churn', legend=False)
    plt.title('Monthly Charges vs Churn Status', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Churn Status', fontsize=12)
    plt.ylabel('Monthly Charges ($)', fontsize=12)
    plt.tight_layout()
    plt.savefig('outputs/boxplot_monthly_charges.png', dpi=300)
    plt.close()

    print("EDA Plots successfully saved to outputs/ directory.")

    # 4. Train / Test Split & Feature Scaling
    X = df_encoded.drop(columns=['Churn'])
    y = df_encoded['Churn']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])

    # Save scaler
    joblib.dump(scaler, 'outputs/scaler.pkl')

    print(f"\n[4] Data Split Completed: Train shape={X_train.shape}, Test shape={X_test.shape}")

    # 5. Supervised Learning Models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Naive Bayes': GaussianNB(),
        'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    }

    results = []

    for name, model in models.items():
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        results.append({
            'Model': name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1 Score': f1
        })

        cm = confusion_matrix(y_test, y_pred)

        # Save confusion matrix image
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                    xticklabels=['Non-Churn', 'Churn'],
                    yticklabels=['Non-Churn', 'Churn'])
        plt.title(f'Confusion Matrix - {name}', fontsize=14, fontweight='bold', pad=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.ylabel('True Label', fontsize=12)
        plt.tight_layout()

        if name == 'Logistic Regression':
            filename = 'outputs/confusion_matrix_lr.png'
        elif name == 'Naive Bayes':
            filename = 'outputs/confusion_matrix_nb.png'
        elif name == 'Decision Tree':
            filename = 'outputs/confusion_matrix_dt.png'
        else:
            filename = 'outputs/confusion_matrix_rf.png'
        plt.savefig(filename, dpi=300)
        plt.close()

        print(f"\n--- {name} Performance ---")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Model Comparison Table
    results_df = pd.DataFrame(results)
    print("\n================ MODEL PERFORMANCE COMPARISON ================")
    print(results_df.to_string(index=False))

    # Save Accuracy Comparison Table visual image
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.axis('off')
    tbl_data = [[row['Model'], f"{row['Accuracy']:.4f}", f"{row['Precision']:.4f}", f"{row['Recall']:.4f}", f"{row['F1 Score']:.4f}"] for _, row in results_df.iterrows()]
    table = ax.table(
        cellText=tbl_data,
        colLabels=['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score'],
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.8)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#2b5c8f')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor('#f2f4f7' if row % 2 == 0 else '#ffffff')
    plt.title('Model Performance Metrics Comparison', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('outputs/accuracy_table.png', dpi=300)
    plt.close()

    # 6. Unsupervised Learning: K-Means Clustering
    print("\n[6] Unsupervised Learning: K-Means Clustering")
    
    X_cluster = df_encoded.copy()
    scaler_kmeans = StandardScaler()
    X_cluster_scaled = scaler_kmeans.fit_transform(X_cluster)

    # Elbow Method
    wcss = []
    K_range = range(1, 11)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_cluster_scaled)
        wcss.append(kmeans.inertia_)

    # Plot Elbow Method graph
    plt.figure(figsize=(8, 5))
    plt.plot(K_range, wcss, marker='o', linestyle='--', color='#2b5c8f', linewidth=2, markersize=8)
    plt.title('Elbow Method For Optimal K', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Number of Clusters (K)', fontsize=12)
    plt.ylabel('Within-Cluster Sum of Squares (WCSS)', fontsize=12)
    plt.axvline(x=3, color='red', linestyle=':', label='Optimal K = 3')
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig('outputs/elbow_method.png', dpi=300)
    plt.close()

    # Fit K-Means with K=3
    optimal_k = 3
    kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans_optimal.fit_predict(X_cluster_scaled)
    df_clean['Cluster'] = cluster_labels

    cluster_stats = df_clean.groupby('Cluster')[['tenure', 'MonthlyCharges', 'TotalCharges']].mean()
    cluster_stats['Churn_Rate (%)'] = df_clean.groupby('Cluster')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    print("\nCluster Profiling Statistics:\n", cluster_stats)

    churn_rates = cluster_stats['Churn_Rate (%)'].to_dict()
    sorted_clusters = sorted(churn_rates.keys(), key=lambda c: churn_rates[c], reverse=True)
    cluster_mapping = {
        sorted_clusters[0]: 'Cluster 1: High-Risk Customers',
        sorted_clusters[1]: 'Cluster 2: Medium-Risk Customers',
        sorted_clusters[2]: 'Cluster 0: Loyal Customers'
    }
    df_clean['Cluster_Name'] = df_clean['Cluster'].map(cluster_mapping)

    # 7. Dimensionality Reduction with PCA
    print("\n[7] Applying PCA for 2D Cluster Visualization...")
    pca = PCA(n_components=2, random_state=42)
    pca_features = pca.fit_transform(X_cluster_scaled)
    df_clean['PCA1'] = pca_features[:, 0]
    df_clean['PCA2'] = pca_features[:, 1]

    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        x='PCA1', y='PCA2', hue='Cluster_Name', data=df_clean,
        palette=['#d62728', '#ff7f0e', '#2ca02c'], alpha=0.7, s=40
    )
    plt.title('Customer Segments Visualized via PCA (K=3)', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% Variance)', fontsize=12)
    plt.ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% Variance)', fontsize=12)
    plt.legend(title='Customer Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('outputs/pca_clusters.png', dpi=300)
    plt.close()

    # 8. Generate Final Prediction Output Sample Graphic
    plt.figure(figsize=(10, 5))
    plt.axis('off')
    sample_df = df_clean[['gender', 'Contract', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn', 'Cluster_Name']].head(8)
    sample_df.columns = ['Gender', 'Contract', 'Tenure', 'Monthly Charge', 'Total Charge', 'Churn', 'Segment']
    
    cell_text = []
    for idx, row in sample_df.iterrows():
        cell_text.append([str(row[c]) for c in sample_df.columns])
        
    table = plt.table(
        cellText=cell_text,
        colLabels=sample_df.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.1, 1.6)
    for (r, c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor('#1f77b4')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor('#f7f9fb' if r % 2 == 0 else '#ffffff')

    plt.title('Sample Customer Churn & Segmentation Output Table', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('outputs/final_prediction_output.png', dpi=300)
    plt.close()

    print("\n[8] All Machine Learning Project Execution Steps Completed Successfully!")
    print("All output plots saved in outputs/ directory.")
    print("=" * 70)

if __name__ == "__main__":
    main()
