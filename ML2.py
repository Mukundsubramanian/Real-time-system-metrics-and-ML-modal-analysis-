import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from statsmodels.tsa.seasonal import seasonal_decompose
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    return df

def detect_anomalies(df):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    anomalies = iso_forest.fit_predict(scaled_data)
    df['anomaly'] = anomalies
    return df

def analyze_time_series(df, column):
    decomposition = seasonal_decompose(df[column], model='additive', period=24)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    return trend, seasonal, residual

def forecast_with_prophet(df, column):
    prophet_df = df.reset_index().rename(columns={'Timestamp': 'ds', column: 'y'})
    prophet_df = prophet_df[['ds', 'y']].dropna()
    model = Prophet()
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    return forecast

def numeric_cluster_analysis(df):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df.drop('anomaly', axis=1))
    
    # Determine optimal number of clusters
    silhouette_scores = []
    for n_clusters in range(2, 11):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(scaled_data)
        silhouette_scores.append(silhouette_score(scaled_data, cluster_labels))
    
    optimal_clusters = silhouette_scores.index(max(silhouette_scores)) + 2
    
    # Perform clustering with optimal number of clusters
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    
    # Analyze cluster characteristics
    df['cluster'] = clusters
    cluster_stats = df.groupby('cluster').agg(['mean', 'std'])
    
    return clusters, cluster_stats, optimal_clusters

def correlation_analysis(df):
    corr_matrix = df.corr()
    return corr_matrix

def anomaly_classification(df):
    features = df.drop(['anomaly', 'cluster'], axis=1)
    labels = df['anomaly']
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    classification_rep = classification_report(y_test, y_pred, output_dict=True)
    return clf, classification_rep

def analyze_logs(file_path):
    df = load_and_prepare_data(file_path)
    df = detect_anomalies(df)
    results = {}
    # Include HBM_Usage in the analysis
    for column in ['CPU', 'GPU', 'Memory_Usage', 'HBM_Usage', 'Data_In', 'Data_Out']:
        trend, seasonal, residual = analyze_time_series(df, column)
        forecast = forecast_with_prophet(df, column)
        results[column] = {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'forecast': forecast
        }
    clusters, cluster_stats, optimal_clusters = numeric_cluster_analysis(df)
    corr_matrix = correlation_analysis(df)
    anomaly_classifier, classification_rep = anomaly_classification(df)
    return df, results, corr_matrix, anomaly_classifier, cluster_stats, classification_rep, optimal_clusters

def interpret_results(df, results, corr_matrix, anomaly_classifier, cluster_stats, classification_rep, optimal_clusters):
    # Include HBM_Usage in the interpretation
    for column in ['CPU', 'GPU', 'Memory_Usage', 'HBM_Usage', 'Data_In', 'Data_Out']:
        print(f"\nAnalysis for {column}:")
        trend = results[column]['trend']
        trend_change = trend.iloc[-1] - trend.iloc[0]
        print(f"Overall trend: {'Increasing' if trend_change > 0 else 'Decreasing'}")
        seasonal = results[column]['seasonal']
        max_seasonal_impact = seasonal.abs().max()
        print(f"Maximum seasonal impact: {max_seasonal_impact:.2f}")
        forecast = results[column]['forecast']
        future_trend = forecast['yhat'].iloc[-1] - forecast['yhat'].iloc[0]
        print(f"Forecasted trend: {'Increasing' if future_trend > 0 else 'Decreasing'}")
    
    print("\nCorrelation Analysis:")
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            correlation = corr_matrix.iloc[i, j]
            if abs(correlation) > 0.5:
                print(f"Strong correlation between {corr_matrix.columns[i]} and {corr_matrix.columns[j]}: {correlation:.2f}")
    
    print(f"\nCluster Analysis (Optimal number of clusters: {optimal_clusters}):")
    print(cluster_stats)
    
    print("\nAnomaly Classification:")
    print(f"Accuracy: {classification_rep['accuracy']:.2f}")
    print(f"Precision: {classification_rep['weighted avg']['precision']:.2f}")
    print(f"Recall: {classification_rep['weighted avg']['recall']:.2f}")
    print(f"F1-score: {classification_rep['weighted avg']['f1-score']:.2f}")
    
    feature_importance = pd.DataFrame({'feature': df.columns[:-2], 'importance': anomaly_classifier.feature_importances_})
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    print("\nTop 3 features for anomaly detection:")
    print(feature_importance.head(3))

if __name__ == "__main__":
    csv_file = 'live_log_dataset.csv'
    df, results, corr_matrix, anomaly_classifier, cluster_stats, classification_rep, optimal_clusters = analyze_logs(csv_file)
    interpret_results(df, results, corr_matrix, anomaly_classifier, cluster_stats, classification_rep, optimal_clusters)
