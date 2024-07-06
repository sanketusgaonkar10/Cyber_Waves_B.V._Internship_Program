import pandas as pd
import numpy as np
from scipy.stats import zscore

# Load and preprocess data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df.dropna(inplace=True)
    return df

# Calculate statistical metrics
def calculate_statistics(df):
    stats = df.groupby('category')['amount'].agg(['mean', 'median', 'std'])
    return stats

# Detect anomalies using Z-score
def detect_anomalies(df, stats, threshold=3):
    df = df.join(stats, on='category')
    df['z_score'] = (df['amount'] - df['mean']) / df['std']
    anomalies = df[(df['z_score'].abs() > threshold) & (df['std'] != 0)]
    anomalies['reason_for_anomaly'] = anomalies.apply(lambda row: f"{row['z_score']:.2f} standard deviations from the mean", axis=1)
    return anomalies

# Generate anomaly report
def generate_report(anomalies):
    report_columns = ['transaction_id', 'date', 'category', 'amount', 'reason_for_anomaly']
    report = anomalies[report_columns].sort_values(by='date')
    report_summary = {
        "total_transactions": len(anomalies),
        "anomalies_detected": len(anomalies),
        "categories_affected": anomalies['category'].nunique()
    }
    return report, report_summary

# Main function to run the anomaly detection process
def main(file_path):
    df = load_data(file_path)
    stats = calculate_statistics(df)
    anomalies = detect_anomalies(df, stats)
    report, report_summary = generate_report(anomalies)

    print("Anomaly Detection Report")
    print(report)
    print("\nSummary Statistics")
    print(report_summary)

# Run the anomaly detection script
if __name__ == "__main__":
    # Replace 'transactions.csv' with your actual CSV file path
    main('transactions.csv')