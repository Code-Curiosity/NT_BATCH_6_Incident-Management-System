from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

from app.database import get_db
from app.models.incident import Incident
from app.models.incident_log import IncidentLog
from app.models.user import User
from app.routes.websocket import manager

# ── Pydantic schema for partial updates ──────────────────────────────────────
class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    incident_type: Optional[str] = None
    status: Optional[str] = None
    assigned_team: Optional[int] = None
    assigned_user: Optional[int] = None
    priority_score: Optional[int] = None
    root_cause: Optional[str] = None
    affected_services: Optional[List[str]] = None

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
    data["logs"] = [{"action": l.action, "timestamp": l.timestamp.isoformat() + "Z", "details": l.details} for l in logs]
    return data

async def _update_status(incident_id: int, status: str, db: Session, extra_details: str = None):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    incident.status = status
    if status == "RESOLVED":
        incident.resolved_at = datetime.utcnow()
        if incident.created_at:
            delta = incident.resolved_at - incident.created_at
            incident.resolution_time = int(delta.total_seconds())
            
    log_msg = f"Status changed to {status}"
    if extra_details:
        log_msg += f". {extra_details}"
        
    db.add(IncidentLog(incident_id=incident_id, action=status, details=log_msg))
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
async def escalate_incident(incident_id: int, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    extra_details = None
    if inc:
        inc.escalation_count += 1
        # Reassign to team lead
        lead = db.query(User).filter(User.team_id == inc.assigned_team, User.role == 'lead').first()
        if lead and inc.assigned_user != lead.id:
            inc.assigned_user = lead.id
            extra_details = f"Escalated to team lead: {lead.name}"
            
    return await _update_status(incident_id, "ESCALATED", db, extra_details)

@router.patch("/{incident_id}/resolve")
async def resolve_incident(incident_id: int, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    extra_details = None
    if inc and inc.assigned_user:
        user = db.query(User).filter(User.id == inc.assigned_user).first()
        if user:
            extra_details = f"Resolved by {user.name}"
    return await _update_status(incident_id, "RESOLVED", db, extra_details)

@router.put("/{incident_id}")
async def update_incident(incident_id: int, data: IncidentUpdate, db: Session = Depends(get_db)):
    """Update incident details (title, description, severity, assignment, etc.)."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    db.add(IncidentLog(incident_id=incident_id, action="UPDATED", details="Incident fields updated"))
    db.commit()
    db.refresh(incident)
    await manager.broadcast({
        "type": "incident_updated",
        "data": incident.to_dict()
    })
    return incident.to_dict()

@router.delete("/{incident_id}", status_code=204)
async def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    """Delete an incident."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    deleted_incident_id = incident.id
    db.delete(incident)
    db.commit()
    await manager.broadcast({
        "type": "incident_deleted",
        "incident_id": deleted_incident_id
    })
    return None
