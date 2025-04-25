import psutil
import time
from datetime import datetime

def get_system_metrics():
    metrics = {
        'cpu': {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(logical=True)
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'percent': psutil.virtual_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'percent': psutil.disk_usage('/').percent
        },
        'network': {
            'bytes_sent': psutil.net_io_counters().bytes_sent,
            'bytes_recv': psutil.net_io_counters().bytes_recv
        },
        'timestamp': datetime.now().isoformat()
    }
    return metrics

def get_process_info():
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
    return processes