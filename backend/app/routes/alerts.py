"""
Alert Ingestion Routes.
Receives raw alerts, classifies them, and creates incidents.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.incident import Incident
from app.routes.websocket import queue_incident_event
from app.services.classification import classify_alert

router = APIRouter()


class AlertInput(BaseModel):
    type: str               # e.g., "server down", "high cpu", "app error"
    message: str            # alert description
    source: str             # "infrastructure" or "application"
    metadata: Optional[dict] = None


@router.post("/ingest", status_code=201)
def ingest_alert(alert: AlertInput, db: Session = Depends(get_db)):
    """
    Ingest a raw alert, classify it, and create an incident.
    This is the main entry point for the event-driven pipeline.
    """
    # Classify the alert
    classification = classify_alert(alert.model_dump())

    # Create incident from classified alert
    incident = Incident(
        title=alert.type,
        description=alert.message,
        severity=classification["severity"],
        status="new",
        assigned_to=classification["assigned_to"],
        source=classification["source"],
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    queue_incident_event("incident_created", incident=incident.to_dict())

    return {
        "message": "Alert ingested and incident created",
        "incident": incident.to_dict(),
        "classification": classification,
    }
