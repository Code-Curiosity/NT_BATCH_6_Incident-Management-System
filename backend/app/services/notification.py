"""
Notification Service.
Handles sending notifications for incident events (email, Slack, SMS stubs).
"""

import logging

logger = logging.getLogger(__name__)


async def notify_incident_created(incident: dict):
    """Send notification when a new incident is created."""
    logger.info(
        f"[NOTIFICATION] New incident #{incident['id']}: "
        f"{incident['title']} | Severity: {incident['severity']} | "
        f"Assigned to: {incident['assigned_to']}"
    )
    # TODO: Integrate with email/Slack/SMS APIs
    # Example: await send_email(on_call_email, incident)
    # Example: await send_slack_message(channel, incident)


async def notify_incident_updated(incident: dict, action: str):
    """Send notification when an incident status changes."""
    logger.info(
        f"[NOTIFICATION] Incident #{incident['id']} {action}: "
        f"Status → {incident['status']}"
    )
    # TODO: Integrate with notification channels


async def notify_escalation(incident: dict):
    """Send escalation notification for unresolved critical incidents."""
    logger.warning(
        f"[ESCALATION] Incident #{incident['id']} requires escalation! "
        f"Severity: {incident['severity']} | "
        f"Assigned to: {incident['assigned_to']}"
    )
    # TODO: Notify senior on-call team / management
