import csv
import random
import time
from datetime import datetime
import psutil
import sqlite3

# CSV file configuration
csv_file = 'live_log_dataset.csv'

# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create a table for storing logs
cursor.execute('''
    CREATE TABLE system_logs (
        timestamp TEXT,
        cpu REAL,
        gpu REAL,
        memory_usage REAL,
        data_in INTEGER,
        data_out INTEGER
    )
''')

def write_to_csv(file_name, data):
    """
    Write data to a CSV file.
    """
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write headers only if the file is empty
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'CPU', 'GPU', 'Memory_Usage', 'Data_In', 'Data_Out'])
        writer.writerow(data)

def simulate_cpu_usage():
    """
    Simulate CPU usage percentage.
    """
    return round(random.uniform(20.0, 90.0), 1)

def simulate_gpu_usage():
    """
    Simulate GPU usage percentage.
    """
    return round(random.uniform(10.0, 80.0), 1)

def simulate_memory_usage():
    """
    Simulate memory usage percentage.
    """
    return psutil.virtual_memory().percent

def simulate_data_transfer():
    """
    Simulate data in and out (in KB).
    """
    data_in = random.randint(500, 5000)  # Data received in KB
    data_out = random.randint(500, 5000)  # Data sent in KB
    return data_in, data_out

def insert_into_database(data):
    """
    Insert log data into the SQLite database.
    """
    cursor.execute('''
        INSERT INTO system_logs (timestamp, cpu, gpu, memory_usage, data_in, data_out)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

def generate_live_logs(num_entries=10):
    """
    Generate live log data and store it in both a CSV file and the SQLite database.
    """
    for _ in range(num_entries):
        # Generate log entry details
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu_usage = simulate_cpu_usage()
        gpu_usage = simulate_gpu_usage()
        memory_usage = simulate_memory_usage()
        data_in, data_out = simulate_data_transfer()

        # Create log entry
        log_entry = [timestamp, cpu_usage, gpu_usage, memory_usage, data_in, data_out]

        # Write log entry to CSV file
        write_to_csv(csv_file, log_entry)

        # Insert log entry into the database
        insert_into_database(log_entry)

        # Simulate some delay between log entries
        time.sleep(random.uniform(0.5, 2.0))

def update_logs_every_15_seconds():
    """
    Update logs every 15 seconds for 2 minutes.
    """
    for _ in range(8):  # 8 updates in 2 minutes (every 15 seconds)
        generate_live_logs(5)  # Generate 5 log entries in each update
        time.sleep(15)  # Wait for 15 seconds before the next update

if __name__ == "__main__":
    print("Generating live log dataset. Press Ctrl+C to stop.")
    try:
        update_logs_every_15_seconds()
    except KeyboardInterrupt:
        print("\nStopped generating log data.")
    finally:
        # Close the database connection
        conn.close()
