from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processes')
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'io_counters']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu_percent': proc.info['cpu_percent'],
                'memory': proc.info['memory_info'].rss // (1024 * 1024),  # Memory in MB
                'disk_read': proc.info['io_counters'].read_bytes if proc.info['io_counters'] else 0,
                'disk_write': proc.info['io_counters'].write_bytes if proc.info['io_counters'] else 0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return jsonify(processes)

if __name__ == '__main__':
    app.run(debug=True)
