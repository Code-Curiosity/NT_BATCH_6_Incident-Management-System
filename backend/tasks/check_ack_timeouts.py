import time
from datetime import datetime
from app.database import SessionLocal
from app.models import Incident, IncidentAssignmentQueue, IncidentLog
from app.services.assignment import try_assign_incident

def run_ack_checker():
    print("[Task] Starting ACK Timeout Checker thread...")
    while True:
        try:
            db = SessionLocal()
            now = datetime.utcnow()
            
            # Find OPEN incidents that passed their ack deadline
            timed_out_incidents = db.query(Incident).filter(
                Incident.status == "OPEN",
                Incident.ack_deadline < now,
                Incident.assigned_user.isnot(None)
            ).all()
            
            for inc in timed_out_incidents:
                print(f"[Ack Check] Incident {inc.id} passed ack deadline. Re-queueing...")
                # Mark previous assignment run as NO_ACK
                q = db.query(IncidentAssignmentQueue).filter(
                    IncidentAssignmentQueue.incident_id == inc.id,
                    IncidentAssignmentQueue.user_id == inc.assigned_user,
                    IncidentAssignmentQueue.result == "PENDING"
                ).first()
                if q:
                    q.result = "SKIPPED_NO_ACK"
                
                # Unassign current
                inc.assigned_user = None
                inc.escalation_count += 1
                db.add(IncidentLog(incident_id=inc.id, action="TIMEOUT", details="Assignee failed to acknowledge in time. Escalated and reassigning."))
                db.commit()
                
                # Try to assign next member
                try_assign_incident(db, inc.id, inc.assigned_team)
                
            db.close()
        except Exception as e:
            print(f"[Task Error] run_ack_checker: {e}")
            
        time.sleep(25)
