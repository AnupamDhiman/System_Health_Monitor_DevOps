import psutil
import time
import configparser
import os
import logging
import sys
from prometheus_client import start_http_server, Gauge, Counter

# ── Config ───────────────────────────────────────────────────────
config = configparser.ConfigParser()
if not os.path.exists('config.ini'):
    print("Error: config.ini not found!")
    exit()
config.read('config.ini')

try:
    CPU_LIMIT  = int(config['Thresholds']['cpu_max'])
    MEM_LIMIT  = int(config['Thresholds']['memory_max'])
    DISK_LIMIT = int(config['Thresholds']['disk_max'])
    INTERVAL   = int(config['Settings']['check_interval'])
    LOG_FILE   = config['Settings']['log_file']
except KeyError as e:
    print(f"Error: Missing key in config.ini: {e}")
    exit()

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

# ── Main ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Start the metrics server on port 8000
    # Prometheus will scrape http://localhost:8000/metrics
    start_http_server(8000)
    logger.info("Prometheus metrics server started on port 8000")
    logger.info(f"Monitoring started | CPU<{CPU_LIMIT}% MEM<{MEM_LIMIT}% DISK<{DISK_LIMIT}% every {INTERVAL}s")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            check_health()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped.")