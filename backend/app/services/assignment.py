from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import User, Incident, IncidentAssignmentQueue, UnacknowledgedIncident

ACK_TIMEOUT_MINUTES = 10
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
    # Check who has already been tried and skipped for this incident
    already_tried = {r[0] for r in db.query(IncidentAssignmentQueue.user_id)
                     .filter(IncidentAssignmentQueue.incident_id == incident_id).all()}

    for user in members:
        if user.id in already_tried:
            continue
            
        if get_active_count(db, user.id) >= MAX_ACTIVE_INCIDENTS:
            db.add(IncidentAssignmentQueue(incident_id=incident_id, user_id=user.id, result="SKIPPED_BUSY"))
            continue

        # Found available user, assign incident
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if incident:
            incident.assigned_user = user.id
            incident.ack_deadline = datetime.utcnow() + timedelta(minutes=ACK_TIMEOUT_MINUTES)
            incident.status = "OPEN"
            
            db.add(IncidentAssignmentQueue(incident_id=incident_id, user_id=user.id, result="PENDING"))
            db.commit()
            return True

    # No capacity in the whole team -> send to unacknowledged queue
    if not db.query(UnacknowledgedIncident).filter(UnacknowledgedIncident.incident_id == incident_id).first():
        db.add(UnacknowledgedIncident(incident_id=incident_id, team_id=team_id))
        db.commit()
    return False