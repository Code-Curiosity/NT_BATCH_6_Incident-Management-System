"""
Alert Simulator Script.
Generates sample alerts to test the incident management pipeline.
Run: python scripts/simulate_alerts.py
"""

import requests
import time
import random

API_URL = "http://localhost:8000/api/alerts/ingest"

# Sample alerts for testing
SAMPLE_ALERTS = [
    # Infrastructure - Critical
    {
        "type": "server down",
        "message": "Production server web-01 is unreachable. Last heartbeat 5 minutes ago.",
        "source": "infrastructure",
        "metadata": {"host": "web-01", "region": "us-east-1"},
    },
    {
        "type": "database failure",
        "message": "MySQL primary instance has crashed. Connections refused on port 3306.",
        "source": "infrastructure",
        "metadata": {"host": "db-primary", "service": "mysql"},
    },
    {
        "type": "network outage",
        "message": "Load balancer lb-02 is unreachable. All traffic failing over to lb-01.",
        "source": "infrastructure",
        "metadata": {"host": "lb-02", "datacenter": "dc-west"},
    },
    # Infrastructure - High
    {
        "type": "high cpu usage",
        "message": "CPU utilization at 95% on app-server-03 for over 10 minutes.",
        "source": "infrastructure",
        "metadata": {"host": "app-server-03", "cpu_percent": 95},
    },
    {
        "type": "disk full warning",
        "message": "Disk usage at 92% on log-server-01. Log rotation may have failed.",
        "source": "infrastructure",
        "metadata": {"host": "log-server-01", "disk_percent": 92},
    },
    {
        "type": "high memory consumption",
        "message": "Memory usage spiked to 88% on worker-node-05.",
        "source": "infrastructure",
        "metadata": {"host": "worker-node-05", "memory_percent": 88},
    },
    # Application - Critical
    {
        "type": "application crash",
        "message": "Payment service crashed with OOM error. Auto-restart failed.",
        "source": "application",
        "metadata": {"service": "payment-service", "error": "OutOfMemoryError"},
    },
    # Application - High
    {
        "type": "high error rate",
        "message": "Error rate for auth-service exceeded 15% in the last 5 minutes.",
        "source": "application",
        "metadata": {"service": "auth-service", "error_rate": "15.3%"},
    },
    {
        "type": "request timeout",
        "message": "API gateway reporting 30% timeout rate on /api/orders endpoint.",
        "source": "application",
        "metadata": {"endpoint": "/api/orders", "timeout_rate": "30%"},
    },
    # Application - Low
    {
        "type": "deprecated API usage",
        "message": "Client app v2.1 still using deprecated /api/v1/users endpoint.",
        "source": "application",
        "metadata": {"endpoint": "/api/v1/users", "client_version": "2.1"},
    },
]


def send_alert(alert):
    """Send a single alert to the ingestion API."""
    try:
        response = requests.post(API_URL, json=alert)
        result = response.json()
        incident = result.get("incident", {})
        print(
            f"✅ [{incident.get('severity', '?').upper():8}] "
            f"#{incident.get('id', '?')} {alert['type']} "
            f"→ {incident.get('assigned_to', '?')}"
        )
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is the server running on port 8000?")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("=" * 60)
    print("🚨 INCIDENT MANAGEMENT - ALERT SIMULATOR")
    print("=" * 60)
    print(f"Sending {len(SAMPLE_ALERTS)} sample alerts...\n")

    for alert in SAMPLE_ALERTS:
        send_alert(alert)
        time.sleep(0.5)  # Small delay between alerts

    print(f"\n{'=' * 60}")
    print("✅ All sample alerts sent! Check the dashboard.")
    print("=" * 60)


if __name__ == "__main__":
    main()
