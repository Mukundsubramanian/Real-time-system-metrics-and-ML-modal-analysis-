from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.seasonal import seasonal_decompose
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

app = Flask(__name__)

# Your code here
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

def plot_results(df, column, trend, seasonal, residual, forecast):
    fig, axes = plt.subplots(4, 1, figsize=(15, 20))
    
    df.plot(y=column, ax=axes[0], title=f'Original {column} Data')
    trend.plot(ax=axes[1], title=f'{column} Trend')
    seasonal.plot(ax=axes[2], title=f'{column} Seasonal')
    residual.plot(ax=axes[3], title=f'{column} Residual')

    plt.tight_layout()
    
    # Save the figure to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Convert to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = load_and_prepare_data(file)
            df = detect_anomalies(df)
            trend, seasonal, residual = analyze_time_series(df, 'CPU')  # Example column
            forecast = forecast_with_prophet(df, 'CPU')
            plot_url = plot_results(df, 'CPU', trend, seasonal, residual, forecast)
            return render_template('result.html', plot_url=plot_url)
    
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)
