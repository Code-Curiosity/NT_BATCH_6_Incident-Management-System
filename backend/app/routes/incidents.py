"""
Incident API Routes.
CRUD operations and status management for incidents.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.incident import Incident

router = APIRouter()


# --- Pydantic Schemas ---

class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str
    assigned_to: Optional[str] = None
    source: Optional[str] = None


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    assigned_to: Optional[str] = None
    source: Optional[str] = None


# --- Endpoints ---

@router.get("/")
def get_all_incidents(db: Session = Depends(get_db)):
    """Get all incidents, ordered by most recent first."""
    incidents = db.query(Incident).order_by(Incident.created_at.desc()).all()
    return [incident.to_dict() for incident in incidents]


@router.get("/{incident_id}")
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    """Get a single incident by ID."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident.to_dict()


@router.post("/", status_code=201)
def create_incident(data: IncidentCreate, db: Session = Depends(get_db)):
    """Create a new incident."""
    incident = Incident(
        title=data.title,
        description=data.description,
        severity=data.severity,
        status="new",
        assigned_to=data.assigned_to,
        source=data.source,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident.to_dict()


@router.patch("/{incident_id}/acknowledge")
def acknowledge_incident(incident_id: int, db: Session = Depends(get_db)):
    """Acknowledge an incident (status: new → acknowledged)."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    if incident.status != "new":
        raise HTTPException(status_code=400, detail="Incident is not in 'new' status")
    incident.status = "acknowledged"
    db.commit()
    db.refresh(incident)
    return incident.to_dict()


@router.patch("/{incident_id}/escalate")
def escalate_incident(incident_id: int, db: Session = Depends(get_db)):
    """Escalate an incident (status → escalated)."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident.status = "escalated"
    db.commit()
    db.refresh(incident)
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
    return incident.to_dict()


@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    """Delete an incident."""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
    return None
