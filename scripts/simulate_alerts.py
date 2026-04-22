import requests
import time

API_URL = "http://localhost:8000/api/alerts"

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
    # Security - Critical
    {
        "type": "multiple unauthorized access attempts",
        "message": "Detected 500+ failed login attempts from IP 192.168.1.100 targeting admin accounts.",
        "source": "security",
        "metadata": {"ip": "192.168.1.100", "target": "admin"},
    },
    # Security - High
    {
        "type": "ssl certificate expiring",
        "message": "Primary domain SSL certificate will expire in less than 24 hours.",
        "source": "security",
        "metadata": {"domain": "api.prod.com", "days_left": 1},
    },
    # Platform - Critical
    {
        "type": "kubernetes cluster failure",
        "message": "Kubelet not ready on 5 production nodes. Cluster scheduling degraded.",
        "source": "platform",
        "metadata": {"cluster": "prod-k8s", "nodes_failed": 5},
    },
    # Platform - High
    {
        "type": "pipeline build failed",
        "message": "Jenkins master pipeline failed on integration tests for the last 3 runs.",
        "source": "platform",
        "metadata": {"pipeline": "core-backend", "consecutive_failures": 3},
    },
    {
        "type": "container crash loop",
        "message": "Pod redis-cache-0 is in CrashLoopBackOff state.",
        "source": "platform",
        "metadata": {"pod": "redis-cache-0", "namespace": "cache"},
    },
    # Infrastructure - Low
    {
        "type": "high log generation rate",
        "message": "Informational: log ingestion rate has increased by 15%, check application verbosity.",
        "source": "infrastructure",
        "metadata": {"service": "ELK-stack"},
    }
]

def send_alert(alert):
    """Send a single alert to the ingestion API."""
    try:
        response = requests.post(API_URL, json=alert)
        result = response.json()
        
        if response.status_code == 200:
            classification = result.get("classification", {})
            print(
                f"✅ [{classification.get('severity', '?').upper():8}] "
                f"#{result.get('incident_id', '?')} {alert.get('type', 'Alert')} "
                f"→ Team #{result.get('assigned_team', '?')} User #{result.get('assigned_user', '?')}"
            )
        else:
             print(f"❌ Failed to ingest alert: {result}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is the server running on port 8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 60)
    print("🚨 INCIDENT MANAGEMENT - ALERT SIMULATOR")
    print("=" * 60)
    print(f"Sending {len(SAMPLE_ALERTS)} sample alerts to Gemini classification API...\n")

    for alert in SAMPLE_ALERTS:
        send_alert(alert)
        time.sleep(2)  # Delay between alerts to observe WebSockets on Frontend

    print(f"\n{'=' * 60}")
    print("✅ All sample alerts sent! Check the React dashboard.")
    print("=" * 60)

if __name__ == "__main__":
    main()
