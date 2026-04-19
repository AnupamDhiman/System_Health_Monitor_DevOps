import psutil
import time
import configparser
import os

# 1. Load the Configuration
config = configparser.ConfigParser()

# Check if the config file exists first
if not os.path.exists('config.ini'):
    print("Error: 'config.ini' not found! Please create it first.")
    exit()

config.read('config.ini')

try:
    # 2. Get values from the config file (Quotes added to fix NameError!)
    CPU_LIMIT = int(config['Thresholds']['cpu_max'])
    MEM_LIMIT = int(config['Thresholds']['memory_max'])
    INTERVAL = int(config['Settings']['check_interval'])
    LOG_FILE = config['Settings']['log_file']
except KeyError as e:
    print(f"Error: Missing section or key in config.ini: {e}")
    exit()

def check_health():
    """Gathers stats and checks against thresholds."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    timestamp = time.strftime('%H:%M:%S')
    
    print(f"[{timestamp}] CPU: {cpu}% | MEM: {mem}%")

    # 3. Check against thresholds from config
    if cpu > CPU_LIMIT:
        print(f"!!! ALERT: CPU Usage ({cpu}%) is above limit ({CPU_LIMIT}%) !!!")
    
    if mem > MEM_LIMIT:
        print(f"!!! ALERT: Memory Usage ({mem}%) is above limit ({MEM_LIMIT}%) !!!")

    # 4. Optional: Log to file
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] CPU: {cpu}% | MEM: {mem}%\n")

if __name__ == "__main__":
    print(f"--- Monitoring Started ---")
    print(f"CPU Limit: {CPU_LIMIT}% | Mem Limit: {MEM_LIMIT}% | Interval: {INTERVAL}s")
    print(f"Logging to: {LOG_FILE}")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            check_health()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
