import psutil
import time
import configparser
import os
from prometheus_client import start_http_server, Gauge, Counter

# 1. Load the Configuration
config = configparser.ConfigParser()

# Check if the config file exists first
if not os.path.exists('config.ini'):
    print("Error: 'config.ini' not found! Please create it first.")
    exit()

config.read('config.ini')

try:
    # 2. Get values from the config file
    CPU_LIMIT = int(config['Thresholds']['cpu_max'])
    MEM_LIMIT = int(config['Thresholds']['memory_max'])
    DISK_LIMIT = int(config['Thresholds']['disk_max'])
    INTERVAL = int(config['Settings']['check_interval'])
    LOG_FILE = config['Settings']['log_file']
except KeyError as e:
    print(f"Error: Missing section or key in config.ini: {e}")
    exit()

# Prometheus Metrics
CPU_USAGE = Gauge('system_cpu_percent', 'Current CPU usage percent')
MEM_USAGE = Gauge('system_memory_percent', 'Current memory usage percent')
DISK_USAGE = Gauge('system_disk_percent', 'Current disk usage percent')
ALERTS_TRIGGERED = Counter('alerts_triggered_total', 'Total number of alerts triggered')

def check_health():
    """Gathers stats and checks against thresholds."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    timestamp = time.strftime('%H:%M:%S')
    
    # Update Prometheus metrics
    CPU_USAGE.set(cpu)
    MEM_USAGE.set(mem)
    DISK_USAGE.set(disk)

    print(f"{timestamp} | INFO | CPU: {cpu}% | MEM: {mem}% | DISK: {disk}%")

    # 3. Check against thresholds from config
    alert_triggered = False
    if cpu > CPU_LIMIT:
        print(f"!!! ALERT: CPU Usage ({cpu}%) is above limit ({CPU_LIMIT}%) !!!")
        alert_triggered = True
    
    if mem > MEM_LIMIT:
        print(f"!!! ALERT: Memory Usage ({mem}%) is above limit ({MEM_LIMIT}%) !!!")
        alert_triggered = True

    if disk > DISK_LIMIT:
        print(f"!!! ALERT: Disk Usage ({disk}%) is above limit ({DISK_LIMIT}%) !!!")
        alert_triggered = True

    if alert_triggered:
        ALERTS_TRIGGERED.inc()

    # 4. Optional: Log to file
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] CPU: {cpu}% | MEM: {mem}% | DISK: {disk}%\n")

if __name__ == "__main__":
    print(f"--- Monitoring Started ---")
    print(f"CPU Limit: {CPU_LIMIT}% | Mem Limit: {MEM_LIMIT}% | Interval: {INTERVAL}s")
    print(f"Logging to: {LOG_FILE}")
    
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    print("Prometheus metrics available on port 8000")
    
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            check_health()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
