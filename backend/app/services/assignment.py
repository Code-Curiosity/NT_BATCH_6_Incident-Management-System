from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import User, Incident, IncidentAssignmentQueue, UnacknowledgedIncident, IncidentLog

ACK_TIMEOUT_MINUTES = 2
MAX_ACTIVE_INCIDENTS = 3

def get_active_count(db: Session, user_id: int) -> int:
    return db.query(Incident).filter(
        Incident.assigned_user == user_id,
        Incident.status.in_(["OPEN", "ACKNOWLEDGED", "IN_PROGRESS"])
    ).count()

def get_team_members_ordered(db: Session, team_id: int) -> list:
    members = db.query(User).filter(User.team_id == team_id).all()
    # Sort by number of active incidents to spread load evenly
    return sorted(members, key=lambda u: get_active_count(db, u.id))

def try_assign_incident(db: Session, incident_id: int, team_id: int) -> bool:
    members = get_team_members_ordered(db, team_id)
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        return False
        
    already_tried = {r[0] for r in db.query(IncidentAssignmentQueue.user_id)
                     .filter(IncidentAssignmentQueue.incident_id == incident_id).all()}

    # Fallback: After 2 missed ACK timeouts, forcefully assign to least busy and auto-ack.
    if incident.escalation_count >= 2 and members:
        user = members[0]
        incident.assigned_user = user.id
        incident.status = "ACKNOWLEDGED"
        db.add(IncidentLog(incident_id=incident_id, action="ACKNOWLEDGED", details=f"Auto-acknowledged and assigned to {user.name} after multiple timeouts."))
        db.commit()
        return True

    for user in members:
        if user.id in already_tried:
            continue
            
        if get_active_count(db, user.id) >= MAX_ACTIVE_INCIDENTS:
            db.add(IncidentAssignmentQueue(incident_id=incident_id, user_id=user.id, result="SKIPPED_BUSY"))
            continue

        # Found available user, assign incident
        incident.assigned_user = user.id
        incident.ack_deadline = datetime.utcnow() + timedelta(minutes=ACK_TIMEOUT_MINUTES)
        incident.status = "OPEN"
        
        db.add(IncidentAssignmentQueue(incident_id=incident_id, user_id=user.id, result="PENDING"))
        db.add(IncidentLog(incident_id=incident_id, action="ASSIGNED", details=f"Assigned to {user.name}"))
        db.commit()
        return True

    # No capacity in the whole team -> send to unacknowledged queue
    if not db.query(UnacknowledgedIncident).filter(UnacknowledgedIncident.incident_id == incident_id).first():
        db.add(UnacknowledgedIncident(incident_id=incident_id, team_id=team_id))
        db.commit()
    return False