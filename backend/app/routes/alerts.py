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
from app.services.classification import classify_alert
from app.services.assignment import get_team_by_name, auto_assign_to_team_member

router = APIRouter()


class AlertInput(BaseModel):
    type: str               # e.g., "server down", "high cpu", "app error"
    message: str            # alert description
    source: str             # "infrastructure" or "application"
    metadata: Optional[dict] = None


@router.post("/ingest", status_code=201)
def ingest_alert(alert: AlertInput, db: Session = Depends(get_db)):
    """
    Ingest a raw alert, classify it, and create an incident with auto-assignment.
    """
    # Classify the alert
    classification = classify_alert(alert.model_dump())

    # Find the appropriate team based on classification
    team = get_team_by_name(classification["assigned_to"], db)
    
    # Auto-assign to a team member
    assigned_user = None
    team_id = None
    if team:
        team_id = team.id
        assigned_user = auto_assign_to_team_member(team.id, db)

    # Create incident from classified alert
    incident = Incident(
        title=alert.type,
        description=alert.message,
        severity=classification["severity"],
        status="new",
        assigned_to=classification["assigned_to"], # Keep legacy string for now
        team_id=team_id,
        user_id=assigned_user.id if assigned_user else None,
        source=classification["source"],
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)

    return {
        "message": "Alert ingested and incident created",
        "incident": incident.to_dict(),
        "classification": classification,
    }
