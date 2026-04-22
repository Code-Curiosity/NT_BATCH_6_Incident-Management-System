from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.incident import Incident
from app.routes.websocket import queue_incident_event
from app.models import Alert, Incident
from app.services.classification import classify_alert
from app.services.assignment import try_assign_incident
from app.routes.websocket import manager

router = APIRouter()

from typing import Optional, Dict, Any
from pydantic import BaseModel

class AlertPayload(BaseModel):
    message: str
    source: str
    type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@router.post("")
async def ingest_alert(payload: AlertPayload, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Save raw alert
    alert = Alert(message=payload.message, source=payload.source)
    db.add(alert)
    db.commit()
    db.refresh(alert)

    # 2. Classify via Gemini
    full_message = payload.message
    if payload.type:
        full_message = f"Type: {payload.type}. {full_message}"
    if payload.metadata:
        full_message = f"{full_message} Attributes: {payload.metadata}"
        
    classification = classify_alert(full_message, payload.source)
    
    # Map teams to integers since we mocked teams 1-4
    team_map = {"INFRASTRUCTURE": 1, "APPLICATION": 2, "PLATFORM": 3, "SECURITY": 4}
    team_id = team_map.get(classification.get("incident_type", "APPLICATION"), 2)

    # 3. Create Incident
    incident = Incident(
        alert_id=alert.id,
        title=classification.get("title", "New Alert"),
        description=classification.get("description", ""),
        severity=classification.get("severity", "MEDIUM"),
        incident_type=classification.get("incident_type", "APPLICATION"),
        priority_score=classification.get("priority_score", 50),
        affected_services=classification.get("affected_services", []),
        assigned_team=team_id,
        source=payload.source,
        status="OPEN"
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    queue_incident_event("incident_created", incident=incident.to_dict())

    # 4. Smart Assignment
    assigned = try_assign_incident(db, incident.id, team_id)
    db.refresh(incident)

    # 5. Broadcast to WS
    await manager.broadcast({
        "type": "NEW_INCIDENT",
        "data": incident.to_dict()
    })

    return {
        "status": "success",
        "incident_id": incident.id,
        "classification": classification,
        "assigned_user": incident.assigned_user,
        "assigned_team": incident.assigned_team,
        "queued": not assigned
    }
