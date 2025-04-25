import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from datetime import datetime

class AnomalyDetector:
    def __init__(self, contamination=0.05):
        self.scaler = StandardScaler()
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.pca = PCA(n_components=3)
        
    def train(self, data):
        """
        Train the anomaly detection model on the given data.
        
        Args:
            data: pandas DataFrame containing the training data
        """
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        # Apply PCA for dimensionality reduction
        pca_data = self.pca.fit_transform(scaled_data)
        
        # Train the Isolation Forest
        self.model.fit(pca_data)
        
    def detect_anomalies(self, data):
        """
        Detect anomalies in the given data.
        
        Args:
            data: pandas DataFrame containing the data to check for anomalies
            
        Returns:
            pandas DataFrame with anomaly scores and predictions
        """
        # Scale the data
        scaled_data = self.scaler.transform(data)
        
        # Apply PCA
        pca_data = self.pca.transform(scaled_data)
        
        # Predict anomalies
        anomaly_scores = self.model.decision_function(pca_data)
        anomaly_predictions = self.model.predict(pca_data)
        
        # Create results DataFrame
        results = pd.DataFrame({
            'timestamp': data.index,
            'anomaly_score': anomaly_scores,
            'anomaly': anomaly_predictions
        })
        
        # Convert anomaly predictions to binary (1 for anomaly, 0 for normal)
        results['anomaly'] = results['anomaly'].apply(lambda x: 1 if x == -1 else 0)
        
        return results

def detect_system_anomalies(data):
    """
    Main function to detect anomalies in system metrics.
    
    Args:
        data: pandas DataFrame containing system metrics
            Expected columns: cpu, gpu, memory_usage, data_in, data_out
    
    Returns:
        pandas DataFrame with anomaly detection results
    """
    # Initialize the detector
    detector = AnomalyDetector()
    
    # Train on historical data (first 80%)
    train_size = int(len(data) * 0.8)
    train_data = data.iloc[:train_size]
    detector.train(train_data)
    
    # Detect anomalies in the full dataset
    results = detector.detect_anomalies(data)
    
    return results