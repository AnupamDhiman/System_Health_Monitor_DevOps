# ?? System Health Monitor & Observability Stack

![CI Status](https://github.com/AnupamDhiman/System_Health_Monitor_DevOps/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Docker Status](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![Grafana Status](https://img.shields.io/badge/Grafana-Monitoring-orange?logo=grafana)

A beginner-friendly DevOps project that monitors your computer's health using a Python agent, Prometheus for data storage, and Grafana for beautiful visualizations.

---

## ?? Overview
This project demonstrates the core "Three Pillars of Observability" (Metrics, Logging, and Tracing) in a simplified way. It acts like a **Medical Monitor** for your PC, tracking CPU, Memory, and Disk usage in real-time.

## ?? Key Features
- **?? Real-time Stats**: Tracks CPU, Virtual Memory, and Disk usage via Python `psutil`.
- **?? Smart Alerting**: Triggers alerts when "Danger Zones" (thresholds) are crossed.
- **?? Automated Dashboards**: Grafana is pre-configured to show your data immediately.
- **?? One-Command Launch**: Everything is containerized with Docker Compose.
- **?? Safety Net**: Automated tests (CI) run every time you change the code.

---

## ?? Getting Started (The Easy Way)

### 1?? Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### 2?? Launch the System
Open your terminal in this folder and run:
```bash
docker-compose up -d --build
```

### 3?? Explore the Dashboards
- **Web Dashboard**: [http://localhost:3000](http://localhost:3000) (User: `admin` / Pass: `admin`)
- **Raw Metrics**: [http://localhost:9090](http://localhost:9090) (Prometheus)

---

## ?? How to Test the "Alerts"
To see the system react to "high stress":
1. Open **`config.ini`**.
2. Change `cpu_max = 75` to **`cpu_max = 1`**.
3. Save the file.
4. Refresh Grafana and watch the **"Total Alerts"** counter climb!

---

## ?? Common Troubleshooting
| Issue | Solution |
| :--- | :--- |
| **Ports already in use** | Ensure no other apps are using ports `3000`, `9090`, or `8000`. |
| **No data in Grafana** | Wait 30 seconds for Prometheus to "scrape" the first metrics. |
| **Docker errors** | Make sure Docker Desktop is running in the background. |

---

## ?? What's Next? (Your DevOps Journey)
This project covered **Monitoring** and **Containerization**. To grow your skills, we recommend these next steps:
1. **Automated Deployment**: Use a tool like Ansible or Terraform to set this up on a remote server.
2. **Cloud Migration**: Host this stack on AWS, Azure, or Google Cloud.
3. **Log Aggregation**: Add **ELK Stack** (Elasticsearch, Logstash, Kibana) to view detailed logs alongside your graphs.

---

## ?? Project Structure
```text
├── monitor.py          # The "Brain" (Metric collection)
├── config.ini          # The "Rules" (Thresholds)
├── Dockerfile          # The "Blueprint" (Container config)
├── docker-compose.yml  # The "Orchestrator" (Running the stack)
├── prometheus.yml      # The "Collector" (Scraping rules)
├── grafana/            # The "Painter" (Dashboards & Visuals)
└── tests/              # The "Safety Check" (Automated tests)
```
