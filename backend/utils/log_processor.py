import pandas as pd
import json
from datetime import datetime

def process_log_file(file_path):
    try:
        # Read the log file
        df = pd.read_csv(file_path)
        
        # Process the data
        processed_data = {
            'summary': {
                'total_records': len(df),
                'start_time': df['Timestamp'].min(),
                'end_time': df['Timestamp'].max(),
                'duration': (df['Timestamp'].max() - df['Timestamp'].min()).total_seconds()
            },
            'metrics': {
                'cpu': {
                    'average': df['CPU'].mean(),
                    'max': df['CPU'].max(),
                    'min': df['CPU'].min()
                },
                'memory': {
                    'average': df['Memory'].mean(),
                    'max': df['Memory'].max(),
                    'min': df['Memory'].min()
                }
            }
        }
        
        return processed_data
        
    except Exception as e:
        return {'error': str(e)}