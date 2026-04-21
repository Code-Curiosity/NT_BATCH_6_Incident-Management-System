"""
simulate_alerts.py
──────────────────
Fires sample alerts at the running API to demonstrate the system.
Run with:  python simulate_alerts.py

Make sure the API is running first:
  uvicorn app.main:app --reload
"""

import requests
import time

BASE_URL = "http://localhost:8000"


SAMPLE_ALERTS = [
    # ── INFRASTRUCTURE INCIDENTS ──────────────────────────────────────────────
    {
        "label": "🔴 INFRA - Critical Server Outage",
        "payload": {
            "source": "prometheus",
            "message": "prod-server-1 is down and unreachable. Health checks failing for 5 minutes.",
            "host": "prod-server-1",
            "service": "web-server",
        },
    },
    {
        "label": "🟠 INFRA - High CPU Spike",
        "payload": {
            "source": "cloudwatch",
            "message": "CPU usage spike to 98% on database server db-primary. Memory overload detected.",
            "host": "db-primary",
            "service": "postgresql",
        },
    },
    {
        "label": "🟠 INFRA - Network Failure",
        "payload": {
            "source": "datadog",
            "message": "High packet loss on network switch sw-core-02. Latency elevated to 800ms.",
            "host": "sw-core-02",
            "service": "network",
        },
    },
    {
        "label": "🟡 INFRA - Disk Space Warning",
        "payload": {
            "source": "nagios",
            "message": "Disk usage warning on backup-server-3. 90% used. Low space remaining.",
            "host": "backup-server-3",
            "service": "storage",
        },
    },

    # ── APPLICATION INCIDENTS ─────────────────────────────────────────────────
    {
        "label": "🔴 APP - Critical Error Rate Spike",
        "payload": {
            "source": "sentry",
            "message": "Error rate spike: 500 errors per minute on /api/checkout endpoint. 503 responses.",
            "host": "app-server-2",
            "service": "checkout-service",
        },
    },
    {
        "label": "🟡 APP - Slow API Response",
        "payload": {
            "source": "newrelic",
            "message": "API response time degraded. /api/search endpoint slow, averaging 8 seconds.",
            "host": "app-server-1",
            "service": "search-service",
        },
    },
    {
        "label": "🟢 APP - Minor Exception",
        "payload": {
            "source": "loggly",
            "message": "Minor exception in email worker job. Low priority - occasional task failure.",
            "host": "worker-01",
            "service": "email-service",
        },
    },
]


def fire_alert(label: str, payload: dict) -> dict:
    print(f"\n{'='*60}")
    print(f"  Sending: {label}")
    print(f"{'='*60}")
    resp = requests.post(f"{BASE_URL}/alert", json=payload)
    resp.raise_for_status()
    data = resp.json()
    inc = data["incident"]
    print(f"  ✅ Created | ID: {inc['id'][:8]}...")
    print(f"     Type     : {inc['type'].upper()}")
    print(f"     Severity : {inc['severity'].upper()}")
    print(f"     Assignee : {inc['assignee']}")
    print(f"     Status   : {inc['status']}")
    return data


def show_all_incidents():
    print(f"\n{'='*60}")
    print("  📋 ALL ACTIVE INCIDENTS")
    print(f"{'='*60}")
    resp = requests.get(f"{BASE_URL}/incidents")
    data = resp.json()
    for inc in data["incidents"]:
        emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(inc["severity"], "⚪")
        print(f"  {emoji} [{inc['severity'].upper()}] {inc['type'][:6].upper()} | {inc['title'][:50]}")
        print(f"       Assignee: {inc['assignee']} | Status: {inc['status']}")
    print(f"\n  Total: {data['total']} incidents")


def demo_lifecycle(incident_id: str):
    """Walk one incident through acknowledge → resolve."""
    print(f"\n{'='*60}")
    print(f"  🔄 LIFECYCLE DEMO for incident {incident_id[:8]}...")
    print(f"{'='*60}")

    time.sleep(1)
    r = requests.post(f"{BASE_URL}/acknowledge/{incident_id}")
    print(f"  ✅ Acknowledged: {r.json()['incident']['status']}")

    time.sleep(1)
    r = requests.post(f"{BASE_URL}/escalate/{incident_id}")
    print(f"  ⬆️  Escalated to: {r.json()['incident']['severity'].upper()}")

    time.sleep(1)
    r = requests.post(f"{BASE_URL}/resolve/{incident_id}")
    print(f"  ✅ Resolved: {r.json()['incident']['status']}")


if __name__ == "__main__":
    print("\n🚨 INCIDENT MANAGEMENT SYSTEM — ALERT SIMULATOR")
    print("Firing sample alerts...\n")

    created_ids = []
    for alert in SAMPLE_ALERTS:
        result = fire_alert(alert["label"], alert["payload"])
        created_ids.append(result["incident_id"])
        time.sleep(0.5)

    show_all_incidents()

    # Demo lifecycle on first (critical) incident
    print("\n\n--- Running lifecycle demo on first incident ---")
    demo_lifecycle(created_ids[0])

    print("\n\n✅ Simulation complete. Check the dashboard!\n")
