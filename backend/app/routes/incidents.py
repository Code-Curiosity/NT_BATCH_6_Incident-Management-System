from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.incident import Incident
from app.routes.websocket import queue_incident_event
from app.models import Incident, IncidentLog
from app.routes.websocket import manager

router = APIRouter()

@router.get("/")
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).order_by(Incident.created_at.desc()).all()
    return {"incidents": [i.to_dict() for i in incidents]}

@router.get("/{incident_id}")
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    logs = db.query(IncidentLog).filter(IncidentLog.incident_id == incident_id).all()
    data = incident.to_dict()
    data["logs"] = [{"action": l.action, "timestamp": l.timestamp.isoformat()} for l in logs]
    return data

async def _update_status(incident_id: int, status: str, db: Session):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    incident.status = status
    if status == "RESOLVED":
        incident.resolved_at = datetime.utcnow()
        if incident.created_at:
            delta = incident.resolved_at - incident.created_at
            incident.resolution_time = int(delta.total_seconds())
            
    db.add(IncidentLog(incident_id=incident_id, action=status, details=f"Status changed to {status}"))
    db.commit()
    db.refresh(incident)
    
    await manager.broadcast({
        "type": "STATUS_CHANGE",
        "data": incident.to_dict()
    })
    return incident.to_dict()

@router.patch("/{incident_id}/acknowledge")
async def acknowledge_incident(incident_id: int, db: Session = Depends(get_db)):
    return await _update_status(incident_id, "ACKNOWLEDGED", db)

@router.patch("/{incident_id}/escalate")
def escalate_incident(incident_id: int, db: Session = Depends(get_db)):
    """Escalate an incident (status → escalated)."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident.status = "escalated"
    db.commit()
    db.refresh(incident)
    queue_incident_event("incident_updated", incident=incident.to_dict())
    return incident.to_dict()


@router.patch("/{incident_id}/resolve")
def resolve_incident(incident_id: int, db: Session = Depends(get_db)):
    """Resolve an incident (status → resolved)."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident.status = "resolved"
    db.commit()
    db.refresh(incident)
    queue_incident_event("incident_updated", incident=incident.to_dict())
    return incident.to_dict()


@router.put("/{incident_id}")
def update_incident(incident_id: int, data: IncidentUpdate, db: Session = Depends(get_db)):
    """Update incident details."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    queue_incident_event("incident_updated", incident=incident.to_dict())
    return incident.to_dict()


@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    """Delete an incident."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    deleted_incident_id = incident.id
    db.delete(incident)
    db.commit()
    queue_incident_event("incident_deleted", incident_id=deleted_incident_id)
    return None
async def escalate_incident(incident_id: int, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    if inc:
        inc.escalation_count += 1
    return await _update_status(incident_id, "ESCALATED", db)

@router.patch("/{incident_id}/resolve")
async def resolve_incident(incident_id: int, db: Session = Depends(get_db)):
    return await _update_status(incident_id, "RESOLVED", db)
