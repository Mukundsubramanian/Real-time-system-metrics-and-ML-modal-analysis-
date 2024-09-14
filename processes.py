import psutil
import GPUtil
import platform
import os
import time
import subprocess

def get_cpu_performance():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        return cpu_percent, cpu_freq.current, cpu_freq.min, cpu_freq.max
    except Exception as e:
        return f"Error retrieving CPU performance: {e}", None, None, None

def get_memory_info():
    try:
        ram = psutil.virtual_memory()
        return ram.percent, ram.total / (1024 ** 3), ram.available / (1024 ** 3)
    except Exception as e:
        return f"Error retrieving memory info: {e}", None, None

def get_disk_info():
    try:
        disk = psutil.disk_usage('/')
        return disk.percent, disk.total / (1024 ** 3), disk.free / (1024 ** 3)
    except Exception as e:
        return f"Error retrieving disk info: {e}", None, None

def get_network_speed():
    try:
        net_before = psutil.net_io_counters()
        time.sleep(1)
        net_after = psutil.net_io_counters()
        download_speed = (net_after.bytes_recv - net_before.bytes_recv) / 1024
        upload_speed = (net_after.bytes_sent - net_before.bytes_sent) / 1024
        return download_speed, upload_speed
    except Exception as e:
        return f"Error retrieving network speed: {e}", f"Error retrieving network speed: {e}"

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No GPU detected."
        gpu_data = []
        for gpu in gpus:
            gpu_data.append({
                'id': gpu.id,
                'name': gpu.name,
                'load': gpu.load * 100,
                'memory_used': gpu.memoryUsed,
                'memory_total': gpu.memoryTotal,
                'temperature': gpu.temperature
            })
        return gpu_data
    except Exception as e:
        return f"Error retrieving GPU info: {e}"

def get_system_logs():
    try:
        logs = []
        if platform.system() == "Linux":
            logs = subprocess.check_output("dmesg | tail -n 10", shell=True).decode().splitlines()
        elif platform.system() == "Windows":
            logs = subprocess.check_output("powershell Get-EventLog -LogName System -Newest 10", shell=True).decode().splitlines()
        return logs
    except Exception as e:
        return [f"Error retrieving system logs: {e}"]

def get_process_info():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            processes.append(proc.info)
        return processes
    except Exception as e:
        return [f"Error retrieving process info: {e}"]

def get_temperature_info():
    try:
        temp_info = psutil.sensors_temperatures()
        if not temp_info:
            return "No temperature sensors found."
        return temp_info.get('coretemp', temp_info)  # Default to available temp sensors
    except Exception as e:
        return f"Error retrieving temperature info: {e}"

def get_services_info():
    try:
        services = []
        if platform.system() == "Linux":
            services = subprocess.check_output("systemctl list-units --type=service --state=running", shell=True).decode().splitlines()
        elif platform.system() == "Windows":
            services = subprocess.check_output("powershell Get-Service | Where-Object {$_.Status -eq 'Running'}", shell=True).decode().splitlines()
        return services
    except Exception as e:
        return [f"Error retrieving services info: {e}"]

def get_applications_info():
    try:
        apps = []
        for proc in psutil.process_iter(['pid', 'name']):
            apps.append(proc.info['name'])
        return apps
    except Exception as e:
        return [f"Error retrieving applications info: {e}"]

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent, battery.power_plugged
        else:
            return None, None
    except Exception as e:
        return f"Error retrieving battery info: {e}", None

def get_system_support_info():
    try:
        support_info = {
            'platform': platform.platform(),
            'architecture': platform.architecture(),
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version()
        }
        return support_info
    except Exception as e:
        return f"Error retrieving system support info: {e}"

def print_system_info():
    print("Fetching system information... Press Ctrl+C to stop.")
    try:
        while True:
            cpu_performance = get_cpu_performance()
            memory_info = get_memory_info()
            disk_info = get_disk_info()
            network_speed = get_network_speed()
            gpu_info = get_gpu_info()
            system_logs = get_system_logs()
            process_info = get_process_info()
            temperature_info = get_temperature_info()
            services_info = get_services_info()
            applications_info = get_applications_info()
            battery_info = get_battery_info()
            support_info = get_system_support_info()
            
            print(f"\nCPU Utilization: {cpu_performance[0]}%")
            print(f"CPU Frequency: {cpu_performance[1]} MHz (Min: {cpu_performance[2]} MHz, Max: {cpu_performance[3]} MHz)")

            print(f"Memory Utilization: {memory_info[0]}%, Total: {memory_info[1]:.2f} GB, Available: {memory_info[2]:.2f} GB")

            print(f"Disk Utilization: {disk_info[0]}%, Total: {disk_info[1]:.2f} GB, Free: {disk_info[2]:.2f} GB")

            print(f"Network Speed: Download: {network_speed[0]:.2f} KB/s, Upload: {network_speed[1]:.2f} KB/s")

            if isinstance(gpu_info, str):
                print(gpu_info)
            else:
                for gpu in gpu_info:
                    print(f"GPU {gpu['id']} - {gpu['name']}:")
                    print(f"  Utilization: {gpu['load']}%")
                    print(f"  Memory Used: {gpu['memory_used']} MB / {gpu['memory_total']} MB")
                    print(f"  Temperature: {gpu['temperature']} °C")

            print("\nSystem Logs:")
            for log in system_logs:
                print(log)

            print("\nProcesses:")
            for proc in process_info:
                print(f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, Memory: {proc['memory_info'].rss / (1024 ** 2):.2f} MB")

            print("\nTemperature Info:")
            if isinstance(temperature_info, str):
                print(temperature_info)
            else:
                for temp in temperature_info:
                    print(f"{temp.label if hasattr(temp, 'label') else 'Sensor'}: {temp.current} °C")

            print("\nServices:")
            for service in services_info:
                print(service)

            print("\nApplications:")
            for app in applications_info:
                print(app)

            if battery_info[0] is not None:
                print(f"\nBattery: {battery_info[0]}%, Plugged In: {'Yes' if battery_info[1] else 'No'}")
            else:
                print("\nNo battery information available.")

            print("\nSystem Support Information:")
            for key, value in support_info.items():
                print(f"{key}: {value}")

            time.sleep(10)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    print_system_info()
