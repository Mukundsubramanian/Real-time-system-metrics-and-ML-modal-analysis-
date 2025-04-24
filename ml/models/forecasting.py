import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta
import numpy as np

class SystemMetricsForecaster:
    def __init__(self, periods=24, frequency='H'):
        """
        Initialize the forecaster with default parameters.
        
        Args:
            periods: Number of periods to forecast
            frequency: Frequency of the forecast (e.g., 'H' for hourly)
        """
        self.periods = periods
        self.frequency = frequency
        self.models = {}
        
    def prepare_data(self, data, metric):
        """
        Prepare data for Prophet model.
        
        Args:
            data: pandas DataFrame containing the data
            metric: Column name of the metric to forecast
            
        Returns:
            pandas DataFrame in Prophet format
        """
        df = data.reset_index()
        df = df.rename(columns={'timestamp': 'ds', metric: 'y'})
        df['ds'] = pd.to_datetime(df['ds'])
        return df[['ds', 'y']]
    
    def train(self, data):
        """
        Train Prophet models for each metric.
        
        Args:
            data: pandas DataFrame containing the training data
        """
        metrics = ['cpu', 'gpu', 'memory_usage', 'data_in', 'data_out']
        
        for metric in metrics:
            metric_data = self.prepare_data(data, metric)
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True
            )
            model.fit(metric_data)
            self.models[metric] = model
    
    def forecast(self, metric):
        """
        Generate forecast for a specific metric.
        
        Args:
            metric: The metric to forecast (e.g., 'cpu', 'gpu')
            
        Returns:
            pandas DataFrame with forecast results
        """
        if metric not in self.models:
            raise ValueError(f"No model trained for metric: {metric}")
            
        model = self.models[metric]
        future = model.make_future_dataframe(periods=self.periods, freq=self.frequency)
        forecast = model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    def get_all_forecasts(self):
        """
        Generate forecasts for all metrics.
        
        Returns:
            Dictionary of forecasts for each metric
        """
        forecasts = {}
        for metric in self.models.keys():
            forecasts[metric] = self.forecast(metric)
        return forecasts

def create_forecast(data):
    """
    Main function to create forecasts for system metrics.
    
    Args:
        data: pandas DataFrame containing system metrics
            Expected columns: cpu, gpu, memory_usage, data_in, data_out
    
    Returns:
        Dictionary of forecast results for each metric
    """
    # Initialize the forecaster
    forecaster = SystemMetricsForecaster()
    
    # Train the models
    forecaster.train(data)
    
    # Get forecasts for all metrics
    forecasts = forecaster.get_all_forecasts()
    
    return forecasts