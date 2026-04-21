import time
from datetime import datetime
from app.database import SessionLocal
from app.models import UnacknowledgedIncident, Incident
from app.services.assignment import try_assign_incident

def run_watcher():
    print("[Task] Starting Queue Watcher thread...")
    while True:
        try:
            db = SessionLocal()
            
            # Get all incidents stuck in unassigned queue
            queued = db.query(UnacknowledgedIncident).filter(
                UnacknowledgedIncident.reassigned_at == None
            ).all()
            
            for q in queued:
                print(f"[Watcher] Attempting to find capacity for queued incident {q.incident_id}...")
                success = try_assign_incident(db, q.incident_id, q.team_id)
                if success:
                    q.reassigned_at = datetime.utcnow()
                    inc = db.query(Incident).filter(Incident.id == q.incident_id).first()
                    if inc:
                        q.reassigned_to = inc.assigned_user
                    db.commit()
            db.close()
            
        except Exception as e:
            print(f"[Task Error] run_watcher: {e}")
            
        time.sleep(30)
