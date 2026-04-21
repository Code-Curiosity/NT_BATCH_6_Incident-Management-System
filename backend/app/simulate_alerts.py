"""
simulate_alerts.py
──────────────────
Fires sample alerts at the running API to demonstrate the system.
Run with:  python simulate_alerts.py

Make sure the API is running first:
  uvicorn main:app --reload
"""

import requests
import time
import random

BASE_URL = "http://localhost:8000"


SAMPLE_ALERTS = [
    # ── INFRASTRUCTURE INCIDENTS ──────────────────────────────────────────────
    {
        "label": "🔴 INFRA - Critical Server Outage",
        "payload": {
            "type": "server down",
            "message": "prod-server-1 is down and unreachable. Health checks failing for 5 minutes.",
            "source": "infrastructure",
            "metadata": {"host": "prod-server-1", "service": "web-server"},
        },
    },
    {
        "label": "🟠 INFRA - High CPU Spike",
        "payload": {
            "type": "high cpu usage",
            "message": "CPU usage spike to 98% on database server db-primary. Memory overload detected.",
            "source": "infrastructure",
            "metadata": {"host": "db-primary", "service": "postgresql"},
        },
    },
    {
        "label": "🟠 INFRA - Network Failure",
        "payload": {
            "type": "network failure",
            "message": "High packet loss on network switch sw-core-02. Latency elevated to 800ms.",
            "source": "infrastructure",
            "metadata": {"host": "sw-core-02", "service": "network"},
        },
    },
    {
        "label": "🟡 INFRA - Disk Space Warning",
        "payload": {
            "type": "low disk space",
            "message": "Disk usage warning on backup-server-3. 90% used. Low space remaining.",
            "source": "infrastructure",
            "metadata": {"host": "backup-server-3", "service": "storage"},
        },
    },

    # ── APPLICATION INCIDENTS ─────────────────────────────────────────────────
    {
        "label": "🔴 APP - Critical Error Rate Spike",
        "payload": {
            "type": "unresponsive service",
            "message": "Error rate spike: 500 errors per minute on /api/checkout endpoint. 503 responses.",
            "source": "application",
            "metadata": {"host": "app-server-2", "service": "checkout-service"},
        },
    },
    {
        "label": "🟡 APP - Slow API Response",
        "payload": {
            "type": "timeout",
            "message": "API response time degraded. /api/search endpoint slow, averaging 8 seconds.",
            "source": "application",
            "metadata": {"host": "app-server-1", "service": "search-service"},
        },
    },
    {
        "label": "🟢 APP - Minor Exception",
        "payload": {
            "type": "exception",
            "message": "Minor exception in email worker job. Low priority - occasional task failure.",
            "source": "application",
            "metadata": {"host": "worker-01", "service": "email-service"},
        },
    },
]


def fire_alert(label: str, payload: dict) -> dict:
    print(f"\n{'='*60}")
    print(f"  Sending: {label}")
    print(f"{'='*60}")
    resp = requests.post(f"{BASE_URL}/api/alerts/ingest", json=payload)
    resp.raise_for_status()
    data = resp.json()
    inc = data["incident"]
    print(f"  ✅ Created | ID: {str(inc['id'])[:8]}...")
    print(f"     Title     : {inc['title'].upper()}")
    print(f"     Severity : {inc['severity'].upper()}")
    print(f"     Assignee : {inc['user_name'] or 'Unassigned'} ({inc['team_name'] or 'No Team'})")
    print(f"     Status   : {inc['status']}")
    return data


def show_all_incidents():
    print(f"\n{'='*60}")
    print("  📋 ALL ACTIVE INCIDENTS")
    print(f"{'='*60}")
    resp = requests.get(f"{BASE_URL}/api/incidents/")
    data = resp.json()
    for inc in data:
        emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(inc["severity"], "⚪")
        print(f"  {emoji} [{inc['severity'].upper()}] {inc['title'][:30].upper()} | {inc['description'][:50] if inc['description'] else ''}")
        print(f"       Assignee: {inc['user_name']} ({inc['team_name']}) | Status: {inc['status']}")
    print(f"\n  Total: {len(data)} incidents")


def demo_lifecycle(incident_id: int):
    """Walk one incident through acknowledge → escalate → resolve."""
    print(f"\n{'='*60}")
    print(f"  🔄 LIFECYCLE DEMO for incident {incident_id}...")
    print(f"{'='*60}")

    time.sleep(1)
    r = requests.patch(f"{BASE_URL}/api/incidents/{incident_id}/acknowledge")
    print(f"  ✅ Acknowledged: {r.json()['status']}")

    time.sleep(1)
    r = requests.patch(f"{BASE_URL}/api/incidents/{incident_id}/escalate")
    print(f"  ⬆️  Escalated to: {r.json()['status']} (Assigned to Head: {r.json()['user_name']})")

    time.sleep(1)
    r = requests.patch(f"{BASE_URL}/api/incidents/{incident_id}/resolve")
    print(f"  ✅ Resolved: {r.json()['status']}")


if __name__ == "__main__":
    print("\n🚨 INCIDENT MANAGEMENT SYSTEM — ALERT SIMULATOR")
    print("Firing sample alerts...\n")

    incidents_data = []
    for alert in SAMPLE_ALERTS:
        try:
            result = fire_alert(alert["label"], alert["payload"])
            incidents_data.append(result["incident"])
        except Exception as e:
            print(f"  ❌ Failed to fire alert: {e}")
        time.sleep(0.5)

    show_all_incidents()

    # Demo lifecycle on first incident if any were created
    if incidents_data:
        print("\n\n--- Running lifecycle demo on first incident ---")
        demo_lifecycle(incidents_data[0]["id"])

    print("\n\n✅ Simulation complete. Check the dashboard!\n")
