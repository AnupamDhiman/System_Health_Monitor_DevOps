import pytest
from unittest.mock import patch

# We test the LOGIC, not the actual CPU/memory values
# (because those change every second — you can't test a moving target)

# ── Test 1: Normal usage, no alerts should trigger ──────────────
def test_no_alert_when_below_limits():
    """If CPU is 50% and limit is 80%, no alert should happen."""
    cpu = 50
    mem = 60
    disk = 70
    cpu_limit = 80
    mem_limit = 85
    disk_limit = 90

    alerts = []

    if cpu > cpu_limit:
        alerts.append("CPU alert")
    if mem > mem_limit:
        alerts.append("MEM alert")
    if disk > disk_limit:
        alerts.append("DISK alert")

    assert alerts == []   # no alerts expected

# ── Test 2: CPU is too high, alert must trigger ──────────────────
def test_alert_when_cpu_too_high():
    """If CPU is 95% and limit is 80%, alert must trigger."""
    cpu = 95
    cpu_limit = 80
    alert_triggered = cpu > cpu_limit
    assert alert_triggered == True

# ── Test 3: Memory is too high, alert must trigger ───────────────
def test_alert_when_memory_too_high():
    mem = 90
    mem_limit = 85
    alert_triggered = mem > mem_limit
    assert alert_triggered == True

# ── Test 4: Exactly at the limit — NO alert (must be strictly over)
def test_no_alert_at_exact_limit():
    cpu = 80
    cpu_limit = 80
    alert_triggered = cpu > cpu_limit   # 80 > 80 is False
    assert alert_triggered == False

# ── Test 5: config.ini values are being read as integers ─────────
def test_config_values_are_integers():
    """Simulates reading config and checks types are correct."""
    import configparser
    import os

    config = configparser.ConfigParser()
    config.read('config.ini')

    cpu_limit = int(config['Thresholds']['cpu_max'])
    mem_limit = int(config['Thresholds']['memory_max'])

    assert isinstance(cpu_limit, int)
    assert isinstance(mem_limit, int)