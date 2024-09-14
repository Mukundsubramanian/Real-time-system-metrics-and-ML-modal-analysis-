import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.seasonal import seasonal_decompose
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def load_and_prepare_data(file_path):
    # Load the data
    df = pd.read_csv(file_path, parse_dates=['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    return df

def detect_anomalies(df):
    # Prepare data for anomaly detection
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    # Use Isolation Forest for anomaly detection
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    anomalies = iso_forest.fit_predict(scaled_data)
    
    df['anomaly'] = anomalies
    return df

def analyze_time_series(df, column):
    # Perform time series decomposition
    decomposition = seasonal_decompose(df[column], model='additive', period=24)
    
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    
    return trend, seasonal, residual

def forecast_with_prophet(df, column):
    # Prepare data for Prophet
    prophet_df = df.reset_index().rename(columns={'Timestamp': 'ds', column: 'y'})
    prophet_df = prophet_df[['ds', 'y']].dropna()

    # Create and fit the model
    model = Prophet()
    model.fit(prophet_df)

    # Make future dataframe for predictions
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    
    return forecast

def plot_results(df, column, trend, seasonal, residual, forecast):
    fig, axes = plt.subplots(6, 1, figsize=(15, 30))

    # Original data with anomalies
    df.plot(y=column, ax=axes[0], title=f'Original {column} Data with Anomalies')
    anomalies = df[df['anomaly'] == -1]
    axes[0].scatter(anomalies.index, anomalies[column], color='red', label='Anomaly')
    axes[0].legend()

    # Trend
    trend.plot(ax=axes[1], title=f'{column} Trend')

    # Seasonal
    seasonal.plot(ax=axes[2], title=f'{column} Seasonal')

    # Residual
    residual.plot(ax=axes[3], title=f'{column} Residual')

    # Forecast
    axes[4].plot(df.index, df[column], label='Actual')
    axes[4].plot(forecast['ds'], forecast['yhat'], color='red', label='Forecast')
    axes[4].fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3)
    axes[4].set_title(f'{column} Forecast')
    axes[4].legend()

    # HBM usage (only for HBM_Usage column)
    if column == 'HBM_Usage':
        axes[5].plot(df.index, df[column], label='HBM Usage')
        axes[5].set_title('HBM Usage Over Time')
        axes[5].legend()

    plt.tight_layout()
    plt.show()

def cluster_analysis(df):
    # Prepare data for clustering
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df.drop('anomaly', axis=1))

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)

    # Perform PCA for visualization
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)

    # Plot clusters
    plt.figure(figsize=(10, 8))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=clusters, cmap='viridis')
    plt.title('Cluster Analysis of Log Data')
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.colorbar(label='Cluster')
    plt.show()

    return clusters

def analyze_logs(file_path):
    df = load_and_prepare_data(file_path)
    
    # Detect anomalies
    df = detect_anomalies(df)
    
    results = {}
    for column in ['CPU', 'GPU', 'Memory_Usage', 'HBM_Usage', 'Data_In', 'Data_Out']:
        # Time series analysis
        trend, seasonal, residual = analyze_time_series(df, column)
        
        # Forecasting
        forecast = forecast_with_prophet(df, column)
        
        # Plot results
        plot_results(df, column, trend, seasonal, residual, forecast)
        
        # Store results
        results[column] = {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'forecast': forecast
        }
    
    # Perform cluster analysis
    clusters = cluster_analysis(df)
    df['cluster'] = clusters
    
    return df, results

def interpret_results(df, results):
    for column in ['CPU', 'GPU', 'Memory_Usage', 'HBM_Usage', 'Data_In', 'Data_Out']:
        print(f"\nAnalysis for {column}:")
        
        # Identify periods of abnormal activity
        abnormal_df = df[df['anomaly'] == -1].reset_index()
        abnormal_periods = abnormal_df.groupby(abnormal_df['Timestamp'].dt.date).size()
        if not abnormal_periods.empty:
            print(f"Dates with abnormal activity: {', '.join(map(str, abnormal_periods.index))}")
        
        # Analyze trend
        trend = results[column]['trend']
        trend_change = trend.iloc[-1] - trend.iloc[0]
        print(f"Overall trend: {'Increasing' if trend_change > 0 else 'Decreasing'}")
        
        # Analyze seasonality
        seasonal = results[column]['seasonal']
        max_seasonal_impact = seasonal.abs().max()
        print(f"Maximum seasonal impact: {max_seasonal_impact:.2f}")
        
        # Analyze forecast
        forecast = results[column]['forecast']
        future_trend = forecast['yhat'].iloc[-1] - forecast['yhat'].iloc[0]
        print(f"Forecasted trend: {'Increasing' if future_trend > 0 else 'Decreasing'}")
    
    # Analyze clusters
    cluster_counts = df['cluster'].value_counts()
    print("\nCluster Analysis:")
    for cluster, count in cluster_counts.items():
        print(f"Cluster {cluster}: {count} entries")
        cluster_data = df[df['cluster'] == cluster]
        for column in ['CPU', 'GPU', 'Memory_Usage', 'HBM_Usage', 'Data_In', 'Data_Out']:
            print(f"  Average {column}: {cluster_data[column].mean():.2f}")

def summarize_analysis(df, results):
    # Summarize overall findings
    print("\nSummary of Analysis:")
    
    # Summary of anomalies
    total_anomalies = (df['anomaly'] == -1).sum()
    print(f"Total anomalies detected: {total_anomalies}")

    # Summary of trends
    for column in ['CPU', 'GPU', 'Memory_Usage', 'HBM_Usage', 'Data_In', 'Data_Out']:
        if column in results:
            trend = results[column]['trend']
            trend_change = trend.iloc[-1] - trend.iloc[0]
            overall_trend = 'Increasing' if trend_change > 0 else 'Decreasing'
            print(f"Overall trend for {column}: {overall_trend}")

    # Summary of seasonal impacts
    for column in ['CPU', 'GPU', 'Memory_Usage', 'HBM_Usage', 'Data_In', 'Data_Out']:
        if column in results:
            seasonal = results[column]['seasonal']
            max_seasonal_impact = seasonal.abs().max()
            print(f"Maximum seasonal impact for {column}: {max_seasonal_impact:.2f}")

    # Summary of clustering
    cluster_counts = df['cluster'].value_counts()
    for cluster, count in cluster_counts.items():
        print(f"Cluster {cluster} contains {count} entries")

if __name__ == "__main__":
    csv_file = 'live_log_dataset.csv'
    df, results = analyze_logs(csv_file)
    interpret_results(df, results)
    summarize_analysis(df, results)
