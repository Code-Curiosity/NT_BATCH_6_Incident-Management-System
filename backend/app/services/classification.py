"""
Alert Classification Engine.
Classifies incoming alerts by severity and routes them to the appropriate team.
"""


def classify_alert(alert_data: dict) -> dict:
    """
    Classify an incoming alert and determine severity + team assignment.

    Args:
        alert_data: Raw alert data with 'type', 'message', 'source' fields.

    Returns:
        dict with 'severity', 'assigned_to', 'source' classification results.
    """
    alert_type = alert_data.get("type", "").lower()
    source = alert_data.get("source", "unknown").lower()

    # Classification rules
    # Infrastructure alerts → higher severity, assigned to DevOps
    # Application alerts → lower severity, assigned to App Team

    if source == "infrastructure":
        severity = _classify_infrastructure_severity(alert_type)
        assigned_to = "DevOps Team"

    elif source == "application":
        severity = _classify_application_severity(alert_type)
        assigned_to = "Application Team"

    else:
        severity = "medium"
        assigned_to = "Unassigned"

    return {
        "severity": severity,
        "assigned_to": assigned_to,
        "source": source,
    }


def _classify_infrastructure_severity(alert_type: str) -> str:
    """
    Classify infrastructure alert severity.
    """

    critical_keywords = ["down", "outage", "failure", "crash", "unreachable"]
    high_keywords = ["high cpu", "high memory", "disk full", "latency"]

    for keyword in critical_keywords:
        if keyword in alert_type:
            return "critical"

    for keyword in high_keywords:
        if keyword in alert_type:
            return "high"

    return "medium"


def _classify_application_severity(alert_type: str) -> str:
    """
    Classify application alert severity.
    """

    critical_keywords = ["unresponsive", "crash", "data loss"]
    high_keywords = ["error rate", "timeout", "exception"]

    for keyword in critical_keywords:
        if keyword in alert_type:
            return "critical"

    for keyword in high_keywords:
        if keyword in alert_type:
            return "high"

    return "low"