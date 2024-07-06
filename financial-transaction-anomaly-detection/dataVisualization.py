import matplotlib.pyplot as plt

def plot_anomalies(df, anomalies):
    plt.figure(figsize=(10, 6))
    for category in df['category'].unique():
        category_data = df[df['category'] == category]
        plt.scatter(category_data['date'], category_data['amount'], label=f"{category} (normal)")

    plt.scatter(anomalies['date'], anomalies['amount'], color='red', label='Anomaly', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Transaction Amount')
    plt.title('Financial Transactions Anomalies')
    plt.legend()
    plt.show()

# In the main function, add:
plot_anomalies(df, anomalies)c