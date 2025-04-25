from flask import Blueprint, jsonify, request, render_template
from backend.app.models.system_metrics import get_system_metrics, get_process_info
from backend.utils.log_processor import process_log_file
from ml.models.anomaly_detection import detect_anomalies
from ml.models.forecasting import create_forecast
import os
from werkzeug.utils import secure_filename
from flask import current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/metrics')
def get_metrics():
    metrics = get_system_metrics()
    return jsonify(metrics)

@main.route('/api/processes')
def get_processes():
    processes = get_process_info()
    return jsonify(processes)

@main.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the file
        processed_data = process_log_file(file_path)
        return jsonify(processed_data)

@main.route('/api/analyze')
def analyze_data():
    data = request.json
    anomalies = detect_anomalies(data)
    forecast = create_forecast(data)
    return jsonify({
        'anomalies': anomalies,
        'forecast': forecast
    })