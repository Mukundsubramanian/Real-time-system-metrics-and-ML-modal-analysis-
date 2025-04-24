import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DEBUG = True
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///system_metrics.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/raw')
    ALLOWED_EXTENSIONS = {'csv', 'log'}
    
    # ML Model paths
    MODEL_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ml/models')
    
    # Log configuration
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/app.log')