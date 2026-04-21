import psutil
import time
import configparser
import os
<<<<<<< HEAD
=======
import logging
import sys
>>>>>>> 047089064aba43b6720b729d2d497faeeef36fda
from prometheus_client import start_http_server, Gauge, Counter

# ── Config ───────────────────────────────────────────────────────
config = configparser.ConfigParser()
if not os.path.exists('config.ini'):
    print("Error: config.ini not found!")
    exit()
config.read('config.ini')

try:
<<<<<<< HEAD
    # 2. Get values from the config file
    CPU_LIMIT = int(config['Thresholds']['cpu_max'])
    MEM_LIMIT = int(config['Thresholds']['memory_max'])
    DISK_LIMIT = int(config['Thresholds']['disk_max'])
    INTERVAL = int(config['Settings']['check_interval'])
    LOG_FILE = config['Settings']['log_file']
=======
    CPU_LIMIT  = int(config['Thresholds']['cpu_max'])
    MEM_LIMIT  = int(config['Thresholds']['memory_max'])
    DISK_LIMIT = int(config['Thresholds']['disk_max'])
    INTERVAL   = int(config['Settings']['check_interval'])
    LOG_FILE   = config['Settings']['log_file']
>>>>>>> 047089064aba43b6720b729d2d497faeeef36fda
except KeyError as e:
    print(f"Error: Missing key in config.ini: {e}")
    exit()

<<<<<<< HEAD
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
=======
# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ── Prometheus Metrics (these are the "gauges" Prometheus reads) ──
# A Gauge is a number that goes up AND down (like CPU %)
cpu_gauge    = Gauge('system_cpu_percent',    'Current CPU usage percent')
mem_gauge    = Gauge('system_memory_percent', 'Current memory usage percent')
disk_gauge   = Gauge('system_disk_percent',   'Current disk usage percent')

# A Counter only goes up (like total alerts fired)
alert_counter = Counter('alerts_triggered_total', 'Total number of alerts triggered')

# ── Health Check ─────────────────────────────────────────────────
def check_health():
    cpu  = psutil.cpu_percent(interval=1)
    mem  = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Update Prometheus gauges
    cpu_gauge.set(cpu)
    mem_gauge.set(mem)
    disk_gauge.set(disk)

    logger.info(f"CPU: {cpu}% | MEM: {mem}% | DISK: {disk}%")

    if cpu > CPU_LIMIT:
        logger.warning(f"ALERT: CPU {cpu}% exceeds {CPU_LIMIT}%")
        alert_counter.inc()

    if mem > MEM_LIMIT:
        logger.warning(f"ALERT: Memory {mem}% exceeds {MEM_LIMIT}%")
        alert_counter.inc()

    if disk > DISK_LIMIT:
        logger.warning(f"ALERT: Disk {disk}% exceeds {DISK_LIMIT}%")
        alert_counter.inc()
>>>>>>> 047089064aba43b6720b729d2d497faeeef36fda

# ── Main ─────────────────────────────────────────────────────────
if __name__ == "__main__":
<<<<<<< HEAD
    print(f"--- Monitoring Started ---")
    print(f"CPU Limit: {CPU_LIMIT}% | Mem Limit: {MEM_LIMIT}% | Interval: {INTERVAL}s")
    print(f"Logging to: {LOG_FILE}")
    
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    print("Prometheus metrics available on port 8000")
    
    print("Press Ctrl+C to stop.")
    
=======
    # Start the metrics server on port 8000
    # Prometheus will scrape http://localhost:8000/metrics
    start_http_server(8000)
    logger.info("Prometheus metrics server started on port 8000")
    logger.info(f"Monitoring started | CPU<{CPU_LIMIT}% MEM<{MEM_LIMIT}% DISK<{DISK_LIMIT}% every {INTERVAL}s")
    print("Press Ctrl+C to stop.\n")

>>>>>>> 047089064aba43b6720b729d2d497faeeef36fda
    try:
        while True:
            check_health()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped.")